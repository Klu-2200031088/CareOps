# SMS Authentication Setup Guide

## Overview
CareOps now includes SMS authentication using Twilio. This allows users to:
- Register with their phone number
- Receive SMS verification codes
- Verify their phone number during registration
- Receive SMS reminders for bookings
- Get SMS notifications for form submissions

## Features Implemented

### 1. **SMS Verification on Registration**
- Users can provide phone number during registration
- 6-digit verification code is sent via SMS
- User must enter code to complete registration
- Code expires after 10 minutes
- Option to resend code

### 2. **Backend Changes**
**New Service:** `backend/app/integrations/sms_service.py`
- `send_sms()` - Send SMS to phone number
- `send_verification_code()` - Send 6-digit code
- `send_booking_reminder()` - Remind about upcoming bookings
- `send_booking_confirmation()` - Confirm booking
- `send_form_reminder()` - Remind about pending forms
- `send_inventory_alert()` - Alert on low inventory

**Updated Models:** `backend/app/models/models.py`
- Added `phone_number` field to User
- Added `is_phone_verified` boolean flag
- Added `verification_code` for SMS codes
- Added `verification_code_expires` timestamp

**Updated Schemas:** `backend/app/schemas/schemas.py`
- Added `phone_number` to UserCreate
- Added `is_phone_verified` to UserResponse
- Added `SMSVerificationRequest` schema

**Updated Routes:** `backend/app/routes/auth.py`
- `POST /api/auth/register` - Now accepts phone_number
- `POST /api/auth/verify-sms` - Verify SMS code
- `POST /api/auth/resend-sms` - Resend verification code
- Enhanced error handling and validation

### 3. **Frontend Changes**
**Updated Register Page:** `frontend/src/app/register/page.tsx`
- Phone number input field (optional)
- Two-step registration flow:
  1. Initial registration with credentials
  2. SMS verification step (if phone provided)
- SMS code input with 6-digit masked display
- Resend code functionality
- Better error messages and user feedback

**Updated API Service:** `frontend/src/services/api.ts`
- `authApi.register()` - Updated to support phone_number
- `authApi.verifySMS()` - Verify SMS code
- `authApi.resendSMS()` - Resend code

## Setup Instructions

### Step 1: Get Twilio Credentials
1. Visit https://www.twilio.com/console/
2. Create a free account or sign in
3. Get your credentials:
   - **Account SID**: Under Account Info
   - **Auth Token**: Under Account Info
   - **Phone Number**: Get a Twilio phone number (under Phone Numbers)

### Step 2: Configure Environment Variables
Update `backend/.env` with your Twilio credentials:

```env
TWILIO_ACCOUNT_SID=AC...your-account-sid...
TWILIO_AUTH_TOKEN=...your-auth-token...
TWILIO_PHONE_NUMBER=+1234567890
```

### Step 3: Update Backend Dependencies
Required packages are already in `requirements.txt`:
- `twilio==8.10.0`
- `requests==2.31.0`

### Step 4: Database Migration
The User table now includes SMS fields. When you restart the application:
1. Backend will automatically create/update tables
2. New accounts will support phone verification
3. Existing accounts can add phone numbers later

## Testing SMS Authentication

### Test Scenario 1: Register with Phone
1. Go to http://localhost:3000/register
2. Fill in:
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Password: `password123`
   - Phone: `+1234567890` (your Twilio test number)
3. Click "Register"
4. Receive SMS with verification code
5. Enter code on verification page
6. Account created and verified!

### Test Scenario 2: Register without Phone
1. Skip the phone number field
2. Click "Register"
3. Automatically redirected to login
4. Phone verification optional

### Test Scenario 3: Resend Code
1. If SMS not received, click "Resend"
2. New code sent to your phone
3. Valid for another 10 minutes

### Backend Testing via API Docs
1. Go to http://localhost:8000/docs
2. Try these endpoints:

**Register with phone:**
```bash
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "pass123",
  "full_name": "John Doe",
  "phone_number": "+1234567890"
}
```

**Verify SMS:**
```bash
POST /api/auth/verify-sms?email=user@example.com
{
  "code": "123456"
}
```

**Resend SMS:**
```bash
POST /api/auth/resend-sms?email=user@example.com
```

## API Response Examples

### Successful Registration with Phone
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "is_phone_verified": false,
  "created_at": "2024-01-15T10:30:00"
}
```

### SMS Verification Success
```json
{
  "status": "success",
  "message": "Phone verified successfully"
}
```

### Error Handling
- **Invalid code**: Returns 400 "Invalid verification code"
- **Expired code**: Returns 400 "Verification code expired"
- **No phone on file**: Returns 400 "No phone number on file"
- **SMS not configured**: Returns skipped status with message

## Architecture Diagram

```
Registration Flow:
┌─────────────┐
│   Frontend  │ (register/page.tsx)
└──────┬──────┘
       │ POST /register {email, pwd, name, phone}
       ▼
┌──────────────────────────────────────┐
│   Backend (auth.py routes)           │
│ 1. Validate inputs                   │
│ 2. Check email exists                │
│ 3. Hash password                     │
│ 4. Generate verification code        │
│ 5. Create user (not verified)        │
│ 6. Send SMS                          │
└──────────┬───────────────────────────┘
           │ SMS Service
           ▼
    ┌──────────────┐
    │   Twilio     │ Send 6-digit code
    └──────────────┘
       SMS received by user
       │
       ▼
   User enters code in UI
       │
       ▼
   POST /verify-sms {code}
       │
       ▼
   Backend verifies code
   Updates is_phone_verified = true
       │
       ▼
   Redirect to login ✅
```

## Integration Points

### Email + SMS Hybrid
Use both email and SMS for:
- **Welcome message**: Email + SMS
- **Booking confirmation**: Email + SMS
- **Form reminders**: Email + SMS (if phone verified)
- **Inventory alerts**: Email + SMS

### Optional Enhancements
1. **SMS-based responses**:
   - "CONFIRM" booking via SMS
   - "CANCEL" appointment via SMS
   - "SUBMIT" form response via SMS

2. **SMS-based 2FA**:
   - Optional 2FA with SMS code
   - Alternative to JWT alone

3. **SMS integration with forms**:
   - Submit forms via SMS
   - Receive form URLs via SMS
   - SMS form reminders

4. **Bulk SMS campaigns**:
   - Send appointment reminders to all users
   - Send booking promotions
   - Send feedback requests

## Troubleshooting

### SMS Not Sending
**Problem**: "SMS not configured" message
**Solution**: 
- Check `.env` file has all 3 Twilio variables
- Restart backend server
- Check Twilio account has credits

### Wrong Phone Format
**Problem**: SMS fails or never arrives
**Solution**:
- Use E.164 format: `+1234567890`
- Include country code
- Test with Twilio test phone first

### Code Expires Too Quickly
**Problem**: User can't enter code in time
**Solution**:
- Current: 10 minutes expiry (configurable in auth.py)
- Change: `timedelta(minutes=10)` to desired value

### Database Error on Register
**Problem**: "Registration failed" error
**Solution**:
- Check backend logs for specific error
- Ensure database tables created (restart backend)
- Check database connection in `.env`

## Security Considerations

1. **Verification Code Security**:
   - 6-digit code = ~1 million possibilities
   - 10-minute expiry limits brute force
   - Rate limiting recommended (future)

2. **Phone Number Storage**:
   - Stored in plain text (consider encryption for production)
   - Can implement hashing/encryption later
   - Only show last 4 digits to users

3. **SMS Privacy**:
   - Twilio handles SMS securely
   - User phone not exposed in API responses
   - Consider GDPR compliance for EU users

4. **Production Recommendations**:
   - Move TWILIO credentials to secure secret manager
   - Implement rate limiting on SMS endpoints
   - Add logging for all SMS sends
   - Monitor Twilio billing

## Next Steps

1. ✅ SMS verification on registration
2. Next: SMS bookings reminders
3. Next: SMS form completion reminders
4. Next: SMS-based response handling
5. Next: SMS 2-factor authentication

## Quick Verification Checklist

After setup, verify:
- [ ] Twilio account created with phone number
- [ ] Credentials in `.env` file
- [ ] Backend restarted
- [ ] Frontend registers with phone
- [ ] SMS code received on phone
- [ ] Code verification works
- [ ] User can login after verification
- [ ] Can resend code if needed

## Support

For SMS service issues:
- Twilio Docs: https://www.twilio.com/docs/sms
- Twilio Support: https://support.twilio.com
- Check backend logs: `backend/` terminal output

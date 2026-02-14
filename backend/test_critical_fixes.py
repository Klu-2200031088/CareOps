"""
Test Data & Validation Script for CareOps Critical Fixes
"""

# FIXTURE: Sample data for testing the critical fixes

SAMPLE_USER = {
    "email": "owner@careops.com",
    "password": "SecurePass123!",
    "full_name": "John Business Owner",
    "phone_number": "+1234567890"
}

SAMPLE_WORKSPACE = {
    "name": "CareOps Demo Clinic",
    "address": "123 Main St, Springfield, IL 62701",
    "timezone": "America/Chicago",
    "contact_email": "clinic@careops.com"
}

SAMPLE_CONTACT = {
    "name": "Sarah Johnson",
    "email": "sarah@email.com",
    "phone": "+9876543210"
}

SAMPLE_BOOKING = {
    "booking_type": "consultation",
    "scheduled_at": "2026-02-20T14:00:00",
    "duration_minutes": 60,
    "location": "Downtown Clinic"
}

SAMPLE_FORM = {
    "name": "Health Intake Form",
    "description": "Please fill out your medical history",
    "required_fields": ["full_name", "date_of_birth", "medical_history"]
}

SAMPLE_INVENTORY = {
    "name": "Consultation Slots",
    "quantity": 10,
    "quantity_per_booking": 1,
    "low_threshold": 2
}

SAMPLE_STAFF = {
    "email": "staff@careops.com",
    "password": "StaffPass123!",
    "full_name": "Emily Helper"
}

# ============================================
# TEST CASES FOR CRITICAL FIXES
# ============================================

TEST_CASES = {
    "1_email_hook_on_booking": {
        "name": "Email Confirmation on Booking Creation",
        "endpoint": "POST /bookings/{workspace_id}/{contact_id}/create",
        "expected_behavior": [
            "✅ Booking is created in database",
            "✅ Email confirmation is sent to contact.email",
            "✅ SMS confirmation is sent to contact.phone (if available)",
            "✅ System message appears in conversation",
            "✅ Response includes booking_id"
        ],
        "test_data": [SAMPLE_WORKSPACE, SAMPLE_CONTACT, SAMPLE_BOOKING],
        "validation": "Check inbox: contact should receive booking confirmation email"
    },
    
    "2_email_hook_on_contact": {
        "name": "Welcome Email on Contact Creation",
        "endpoint": "POST /contacts/{workspace_id}/create",
        "expected_behavior": [
            "✅ Contact is created in database",
            "✅ Conversation is created automatically",
            "✅ System welcome message is added to conversation",
            "✅ Welcome email is sent to contact.email",
            "✅ Welcome SMS is sent to contact.phone (if available)",
            "✅ Response includes contact_id"
        ],
        "test_data": [SAMPLE_WORKSPACE, SAMPLE_CONTACT],
        "validation": "Contact should receive welcome email immediately after creation"
    },
    
    "3_automation_on_booking": {
        "name": "Automation Triggers on Booking Creation",
        "endpoint": "POST /bookings/{workspace_id}/{contact_id}/create",
        "expected_behavior": [
            "✅ Booking confirmation email sent (integration with email_service)",
            "✅ SMS confirmation sent (if phone available)",
            "✅ Form reminder triggered (if forms exist)",
            "✅ Conversation message logged",
            "✅ Inventory deducted automatically"
        ],
        "test_data": [SAMPLE_WORKSPACE, SAMPLE_CONTACT, SAMPLE_BOOKING, SAMPLE_FORM],
        "validation": "All emails/SMS should be sent without errors"
    },
    
    "4_staff_role_enforcement": {
        "name": "Staff Role Enforcement in Inbox",
        "endpoint": "GET /inbox/{workspace_id}/conversations",
        "expected_behavior": [
            "✅ Owner can access inbox (always)",
            "✅ Staff with 'inbox' permission can access inbox",
            "✅ Staff without 'inbox' permission cannot access inbox",
            "✅ Non-staff user cannot access inbox",
            "✅ Returns 403 Forbidden for unauthorized access"
        ],
        "test_data": [SAMPLE_WORKSPACE, SAMPLE_STAFF],
        "validation": "Role checker should enforce permissions correctly"
    },
    
    "5_staff_reply_automation": {
        "name": "Automation Pause on Staff Reply",
        "endpoint": "POST /inbox/{workspace_id}/conversations/{conversation_id}/send",
        "expected_behavior": [
            "✅ Staff message is created with sender_type='staff'",
            "✅ Conversation.updated_at is updated",
            "✅ automation_service.on_staff_reply() is triggered",
            "✅ Future automated reminders respect this flag",
            "✅ Response includes message_id"
        ],
        "test_data": [SAMPLE_WORKSPACE, SAMPLE_CONTACT, {"sender_type": "staff", "content": "We received your inquiry", "channel": "system"}],
        "validation": "Automation should pause after staff intervention"
    },
    
    "6_workspace_activation_validation": {
        "name": "Workspace Activation Validation",
        "endpoint": "POST /workspace/{workspace_id}/activate",
        "expected_behavior": [
            "✅ Verify at least one booking type exists",
            "✅ Verify communication channel (email) is configured",
            "✅ Verify at least one form exists",
            "✅ Return error with specific missing requirements",
            "✅ Only activate if all checks pass"
        ],
        "test_data": [SAMPLE_WORKSPACE, SAMPLE_BOOKING, SAMPLE_FORM],
        "validation": "Should reject activation if requirements are missing"
    },
    
    "7_dashboard_form_queries": {
        "name": "Dashboard Form Status Queries",
        "endpoint": "GET /dashboard/{workspace_id}",
        "expected_behavior": [
            "✅ pending_forms count includes only pending forms",
            "✅ overdue_forms count includes overdue pending forms",
            "✅ completed_forms count includes completed forms",
            "✅ All queries filter by workspace_id",
            "✅ Alerts include overdue forms warning"
        ],
        "test_data": [SAMPLE_WORKSPACE, SAMPLE_BOOKING, SAMPLE_FORM],
        "validation": "Form counts should be accurate in dashboard response"
    }
}

# ============================================
# DEPLOYMENT CHECKLIST
# ============================================

DEPLOYMENT_CHECKLIST = [
    {
        "id": 1,
        "task": "Verify all 4 critical files compile without errors",
        "status": "✅ DONE",
        "file": "See error check output above"
    },
    {
        "id": 2,
        "task": "Test email configuration in .env",
        "status": "⏳ TODO",
        "note": "SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD"
    },
    {
        "id": 3,
        "task": "Test SMS configuration in .env",
        "status": "⏳ TODO",
        "note": "TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER"
    },
    {
        "id": 4,
        "task": "Run end-to-end flow test",
        "status": "⏳ TODO",
        "flow": "Register → Create Workspace → Create Contact → Create Booking → Check Inbox"
    },
    {
        "id": 5,
        "task": "Record demo video (4-5 min)",
        "status": "⏳ TODO",
        "coverage": "Show automation triggers, staff replies, dashboard alerts"
    },
    {
        "id": 6,
        "task": "Deploy frontend to Vercel",
        "status": "⏳ TODO",
        "link": "Will be provided after deployment"
    },
    {
        "id": 7,
        "task": "Deploy backend to Render",
        "status": "⏳ TODO",
        "link": "Will be provided after deployment"
    },
    {
        "id": 8,
        "task": "Submit to Telegram group",
        "status": "⏳ TODO",
        "deadline": "Saturday by 11:59 PM"
    }
]

if __name__ == "__main__":
    print("🧪 CareOps Critical Fixes - Test Data\n")
    print("=" * 60)
    for key, test in TEST_CASES.items():
        print(f"\n📝 {key}: {test['name']}")
        print(f"   Endpoint: {test['endpoint']}")
        print(f"   Expected: {len(test['expected_behavior'])} checks")
    
    print("\n\n✅ Deployment Checklist:")
    for item in DEPLOYMENT_CHECKLIST:
        print(f"{item['id']}. {item['task']} - {item['status']}")

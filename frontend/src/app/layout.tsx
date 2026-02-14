import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CareOps - Unified Operations Platform",
  description: "Single platform for all your business operations",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

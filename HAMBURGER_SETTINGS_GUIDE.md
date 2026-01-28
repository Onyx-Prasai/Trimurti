# Hamburger Menu Settings Guide

## Overview
The hamburger icon in the BloodHub navbar now includes a comprehensive **Settings** dropdown menu with multiple configuration options for users. This feature is accessible on mobile devices and provides quick access to various account and application settings.

---

## Settings Features

### 1. **Account Settings** 👤
- **Icon:** FaUser
- **Action:** account
- **Purpose:** Manage user profile information
- **Includes:**
  - Update personal information (name, email, phone)
  - Change email address
  - Edit profile picture
  - Update emergency contacts
  - Verify identity/documents

---

### 2. **Privacy & Security** 🔒
- **Icon:** FaShieldAlt
- **Action:** security
- **Purpose:** Manage account security and privacy
- **Includes:**
  - Change password
  - Enable Two-Factor Authentication (2FA)
  - View login history
  - Manage connected devices
  - Security alerts and notifications
  - Privacy preferences
  - Data usage permissions

---

### 3. **Notification Settings** 🔔
- **Icon:** FaBell
- **Action:** notifications
- **Purpose:** Control how and when users receive notifications
- **Toggle Feature:** Enable/Disable notifications globally
- **Includes:**
  - Email notifications
  - SMS alerts
  - Push notifications
  - Blood request alerts
  - Donation reminders
  - Reward notifications
  - Daily/Weekly digest options
  - Notification frequency control

---

### 4. **Blood Donation Profile** 🩸
- **Icon:** FaTint
- **Action:** donation
- **Purpose:** Manage blood donation-related information
- **Includes:**
  - Blood type confirmation
  - Donation history
  - Medical history and conditions
  - Allergies and medications
  - Weight and health status
  - Preferred donation centers
  - Donation preferences
  - Restriction acknowledgments

---

### 5. **Payment Methods** 💳
- **Icon:** FaCreditCard
- **Action:** payment
- **Purpose:** Manage payment information for rewards/services
- **Includes:**
  - Add/Remove credit/debit cards
  - Add bank accounts
  - Set default payment method
  - View transaction history
  - Manage payment limits
  - E-wallet integration
  - Refund preferences

---

### 6. **Language Settings** 🌐
- **Icon:** FaLanguage
- **Action:** language
- **Purpose:** Change application language
- **Supported Languages:**
  - English (EN)
  - Nepali (NE)
  - Hindi (HI) [Optional]
- **Includes:**
  - Interface language selection
  - Content language preference
  - Regional settings

---

### 7. **Dark Mode** 🌙
- **Icon:** FaMoon
- **Action:** darkmode
- **Purpose:** Toggle between light and dark themes
- **Toggle Feature:** Enable/Disable dark mode
- **Benefits:**
  - Reduces eye strain in low-light conditions
  - Better battery life on OLED screens
  - Improved accessibility
  - User preference persistence

---

### 8. **Help & Support** ❓
- **Icon:** FaQuestionCircle
- **Action:** help
- **Purpose:** Access support resources and documentation
- **Includes:**
  - FAQ section
  - Troubleshooting guides
  - Video tutorials
  - Contact support form
  - Live chat with support team
  - Submit bug reports
  - Feature requests

---

### 9. **Legal & Privacy Policy** 📄
- **Icon:** FaFileAlt
- **Action:** legal
- **Purpose:** View legal documents and privacy information
- **Includes:**
  - Terms and Conditions
  - Privacy Policy
  - Data Protection Information
  - Cookie Policy
  - License Information
  - Liability Disclaimers
  - Compliance Certifications

---

## UI/UX Details

### Hamburger Menu Structure:
```
┌─────────────────────────────────┐
│ ☰ (Menu Icon)                   │
├─────────────────────────────────┤
│ 🏠 Home                          │
│ 🩸 Find Blood                    │
│ 📊 Blood Prediction              │
│ 🩸 Blood Request                 │
│ 👤 Profile                       │
├─────────────────────────────────┤
│ ⚙️  Settings                    ▼│ (Expandable)
│   ├─ 👤 Account Settings         │
│   ├─ 🔒 Privacy & Security       │
│   ├─ 🔔 Notification Settings    │
│   ├─ 🩸 Blood Donation Profile   │
│   ├─ 💳 Payment Methods          │
│   ├─ 🌐 Language                 │
│   ├─ 🌙 Dark Mode                │
│   ├─ ❓ Help & Support           │
│   └─ 📄 Legal & Privacy Policy   │
├─────────────────────────────────┤
│ 🚪 Logout (Red Button)           │
└─────────────────────────────────┘
```

### Styling:
- **Primary Colors:** Uses application's primary color for active items
- **Hover Effects:** Smooth gray background on hover
- **Transitions:** Smooth animations for expand/collapse
- **Icons:** Clear, recognizable Font Awesome icons
- **Spacing:** Proper padding and margins for easy tapping on mobile

---

## State Management

### useState Hooks:
```javascript
const [mobileMenuOpen, setMobileMenuOpen] = useState(false)      // Main menu toggle
const [settingsOpen, setSettingsOpen] = useState(false)         // Settings submenu toggle
const [darkMode, setDarkMode] = useState(false)                 // Dark mode toggle
const [notificationsEnabled, setNotificationsEnabled] = useState(true) // Notifications toggle
```

---

## Action Handlers

The `handleSettingAction(action)` function processes each settings option:

```javascript
const handleSettingAction = (action) => {
  switch(action) {
    case 'account': // Navigate to account settings page
    case 'security': // Open security settings modal
    case 'notifications': // Toggle notifications + show feedback
    case 'donation': // Open blood donation profile
    case 'payment': // Open payment methods page
    case 'language': // Open language selector
    case 'darkmode': // Toggle dark mode + apply theme
    case 'help': // Open help center
    case 'legal': // Open legal documents
  }
  setSettingsOpen(false) // Close settings menu after action
}
```

---

## Implementation Notes

### Current Implementation:
- ✅ Settings menu structure created
- ✅ All icons imported and assigned
- ✅ Toggle functionality for Dark Mode and Notifications
- ✅ Smooth animations with Framer Motion
- ✅ Mobile responsive design
- ⏳ Action handlers use alerts (placeholder)

### To-Do Items:
1. **Create dedicated pages/modals for each setting**
2. **Implement API integration for saving preferences**
3. **Add local storage persistence for settings**
4. **Create backend endpoints for:**
   - Account settings updates
   - Privacy & security management
   - Notification preferences
   - Payment method storage
5. **Implement actual dark mode theme switching**
6. **Add language localization system**
7. **Create support ticket system**
8. **Add proper error handling and validation**

---

## Future Enhancements

1. **Settings Persistence:** Save user preferences to backend
2. **Profile Synchronization:** Sync settings across devices
3. **Settings Search:** Quick search within settings
4. **Settings Export:** Download all settings as JSON
5. **Settings Import:** Upload previous settings
6. **Accessibility Settings:** Font size, contrast, screen reader
7. **Theme Customization:** Custom color schemes
8. **Notification Scheduling:** Quiet hours and notification scheduling
9. **Two-Factor Authentication:** SMS, Email, Authenticator app options
10. **Session Management:** View and revoke active sessions

---

## Security Considerations

1. **Password Requirements:**
   - Minimum 8 characters
   - Mix of uppercase, lowercase, numbers, special characters
   - Password strength indicator

2. **Two-Factor Authentication (2FA):**
   - SMS-based verification
   - Email-based verification
   - Authenticator app support

3. **Data Privacy:**
   - GDPR compliance
   - Data encryption
   - Secure data deletion
   - Regular security audits

4. **Access Control:**
   - Session timeouts
   - IP whitelisting option
   - Device fingerprinting
   - Login notifications

---

## File Locations

- **Component:** [frontend/src/components/Navbar.jsx](frontend/src/components/Navbar.jsx)
- **Settings Configuration:** Defined within Navbar.jsx
- **Icons Library:** React Icons (Font Awesome)

---

## Testing Checklist

- [ ] Settings menu opens/closes correctly
- [ ] All icons display properly
- [ ] Dark mode toggle works
- [ ] Notifications toggle works
- [ ] Settings submenu animations are smooth
- [ ] Mobile responsiveness verified
- [ ] Logout button functions correctly
- [ ] No console errors or warnings
- [ ] Accessibility (keyboard navigation, screen readers)
- [ ] Touch interactions on mobile devices

---

## Code Example

```jsx
const settingsMenuItems = [
  { label: 'Account Settings', icon: FaUser, action: 'account' },
  { label: 'Privacy & Security', icon: FaShieldAlt, action: 'security' },
  { label: 'Notification Settings', icon: FaBell, action: 'notifications' },
  { label: 'Blood Donation Profile', icon: FaTint, action: 'donation' },
  { label: 'Payment Methods', icon: FaCreditCard, action: 'payment' },
  { label: 'Language', icon: FaLanguage, action: 'language' },
  { label: 'Dark Mode', icon: FaMoon, action: 'darkmode' },
  { label: 'Help & Support', icon: FaQuestionCircle, action: 'help' },
  { label: 'Legal & Privacy Policy', icon: FaFileAlt, action: 'legal' },
]
```

---

## Conclusion

The enhanced hamburger menu settings provide a comprehensive, user-friendly interface for managing all account and application settings. The modular design allows for easy expansion and integration with backend services.

**Last Updated:** January 28, 2026
**Status:** ✅ UI Implementation Complete | ⏳ Backend Integration Pending

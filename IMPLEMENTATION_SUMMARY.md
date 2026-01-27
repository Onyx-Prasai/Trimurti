# Implementation Summary

## Registration Bug Fix

A bug in the user registration process that caused a 500 Internal Server Error has been fixed.

### Problem

The backend was only creating a `DonorProfile` for new users with the `base_user` type. When a user registered as a `hospital` or `bloodbank`, no corresponding profile was created. This likely caused a crash in a subsequent part of the application that expected a profile to exist, leading to the 500 error and the frontend receiving an HTML error page instead of a JSON response.

### Solution

The `register_view` in `backend/users/views.py` has been updated to create the appropriate profile (`HospitalProfile`, `BloodBankProfile`, or `AdminProfile`) based on the `user_type` provided during registration. This ensures that every user has a corresponding profile, resolving the root cause of the error.
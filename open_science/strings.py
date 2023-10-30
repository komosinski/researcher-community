# REVIEW routes_def.py
NOT_ENOUGH_RESEARCHERS = 'There are not enough researchers with similar research profiles\
in the system to review this paper. \
    We will wait until more similar researchers are available. \
        You can help with peer review \
            by inviting your colleagues to join researcher.community!'


# REVIEW forms.py

EVALUATION_NOVEL = 'Novel and substantial compared to previous papers \
            by the author(s) and the existing literature'

EVALUATION_JUSTIFIED = 'Claims and conclusions reasonable and justified'

EVALUATION_NOERRORS = 'Free of essential and technical errors'

EVALUATION_WELLPRESENTED = 'Well organized, well presented, readable'

EVALUATION_ACCEPT = 'Accept (the paper may not be perfect, \
            but is free from any serious problems)'

# User blueprint routes.py
USER_NOT_EXISTS = 'User does not exist.'

REMARKS_SAVED = 'Remarks have been saved.'

EDIT_PROFILE_CHANGES_SAVED = 'Your changes have been saved.'

EMAIL_INVITATION_SENT = 'An invitation email has been sent.'

INVITATION_EMAIL_ALREADY_SENT = 'An invitation email to this person has already been sent.'

USER_ALREADY_EXISTS = 'A user with this e-mail already exists.'

INVITATION_DAILY_LIMIT_EXC = 'Daily limit for invitations has been exceeded.'

ENDORSEMENT_REQUEST_SENT = 'The endorsement request was successfully sent.'

CANT_REQUEST_ENDORSEMENT = 'You cannot send your endorsement request (limit exceeded).'

ENDORSEMENT_REQUEST_NOT_EXISTS = 'The endorsement request does not exist.'

ENDORSEMENT_REQUEST_ALREADY_CONSIDERED = 'The endorsement request has already been considered.'

FLASH_TEST_VERISON = 'This is a test version.'

CP_NOT_EXISTS = 'Calibration paper does not exist.'

CP_DELETE_FAILED = 'Calibration paper removal failed'

CP_DELETE_SUCCESS = 'Calibration paper removed successfully'

# Auth blueprint routes.py
EMAIL_CONFIRM_LINK_SENT = ' A confirmation link has been sent to your email address: '

ACC_CONFIRM_DAILY_LIMIT_EXC = 'Daily limit for account confirmation emails has been exceeded. \
                    Check your SPAM folder or try again tomorrow.'

EMAIL_RECOVERY_SENT = 'The account recovery email has been sent'

EMAIL_CONFIRM_EMAIL_SENT = 'A new confirmation email has been sent.'

PASSWORD_CHANGED_SUCCESSFULLY = 'Your password has been successfully changed.'

INVALID_REVOVERY_LINK = 'The account recovery link is invalid or has expired.'

INVALID_CONFIRM_LINK = 'The confirmation link is invalid or has expired.'

ACCOUNT_ALREADY_CONFIRMED = 'Account already confirmed. Please login.'

ACCOUNT_CONFIRMED = 'You have confirmed your account.'

STH_WENT_WRONG = 'Something went wrong.'

EMAIL_DELETE_ACCOUNT_SENT = 'The profile deletion email was sent.'

ACCOUNT_DELETED_SUCCESSFULLY = 'You have deleted your profile.'

EMAIL_CHANGED = 'You have changed your email address.'

READOLNY_SIGNIN_DISABLED = "This website is currently in the read-only mode and Sign-in is disabled"

READOLNY_SIGNUP_DISABLED = "This website is currently in the read-only mode and Sign-up is disabled"

# (completed by researcher)
ENDORSEMENT_REQUEST_FORM_COMPLETED = 'The form has been completed.'

#   login_page

ALREADY_LOGGED = 'You are already logged in.'

LOGIN_SUCCESS = 'You logged in.'

EMAIL_PASSWORD_NOT_MATCH = 'Email and password do not match! Please try again.'

CONFIRM_YOUR_ACCOUNT = 'Please confirm your account!'

PROFILE_IS_DELETED = 'The profile is deleted.'

# USER forms.py
CHECK_READ_BEFORE_PROFILE_DELETE = "I have read the information stated above and understand the implications of having my profile deleted."

# forms.py
DECLARATION_RIGHTS = "I certify that this is original and not published anywhere else \
            (except from venues not restricting publication on this site such as preprint servers, \
                 private websites, conferences and journals with permissive agreements, etc.)"

DECLARATION_AUTHORS = "All authors read and approved the final manuscript"

DECLARATION_NO_INTEREST_CONFLICT = "The authors declare that they have no conflict of interest"

DECLARATION_ANONYMITY = "I certify that this version is anonymized"

DECLARATION_REVIEW = "I would like this paper reviewed"

# utils.py
ADMIN_ROLE_REQUIRED = 'You must be an admin to access this page.'

RESEARCHER_ROLE_REQUIRED = 'You must be a researcher user to access this page.'

# Main blueprint routes.py
READOLNY_LOGOUT_INFO = "You have been logged out because the website is currently in the read-only mode."


# Tag blueprint routes.py
CANT_EDIT_TAG = "You can't edit this tag"

# Review blueprint routes.py
CANT_EDIT_REVIEWERS = "You can't edit the reviewers of this paper"

REVIEWERS_ADDED = "Reviewers have been added"

# Paper routes.py
PAPER_WORD_COUNT_ERROR = "Failed to extract text from paper"
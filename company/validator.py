from django.core.validators import RegexValidator


# Define a validator for GST numbers
gst_validator = RegexValidator(
    regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Za-z]{1}[Z]{1}[0-9A-Za-z]{1}$',
    message='Please enter a valid GST number'
)

# Define a validator for PAN numbers
pan_validator = RegexValidator(
    regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
    message='Please enter a valid PAN number'
)

# Define a validator for contact numbers
contact_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='Please enter a 10-digit phone number'
)

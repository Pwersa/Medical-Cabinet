### GUIDE FOR CONFIGURATION DESCRIPTIONS in config.json

# SET THE EXACT DATA PLEASE
# Check the data types before editing the file

# DATA TYPES #
# STRING = companion_app_IP, email
# INT = port_1st, port_2nd, port_3rd, debug_time_send
# BOOLEAN = connection_mode, email_connection, enable_camera, enable_solenoid, allow_saving_csv

# DESCRIPTIONS #
# connection_mode ---> Enable the connection to the Desktop Companion App 
# companion_app_IP ---> The ip address of the computer that have the Desktop Companion App (receiver)
# port_1st ---> The port for the 1st send of data (responder)
# port_2nd ---> The port for the 2nd send of data (all session including unsent data)
# port_3rd ---> The port for the 3rd send of data (unsent data)
# email_connection ---> Use to enable sending emails (only on the first send, the responder)
# email ---> The email address of the receiver of the email
# enable_camera ---> Enable the camera to scan QR Code (if this is disabled, a static data will be sent)
# enable_solenoid ---> Enable the solenoid to lock and unlock (for the window of the cabinet)
# allow_saving_csv ---> Enable to save the data of ever session (will overite existing file)
# files_not_sent_responder ---> List of data where not sent on responder (primary key is date time)
# files_not_sent_session ---> List of data where not sent on session (primary key is date time)
# whitelisted ---> People that are registered in the whitelist can access this cabinet, even if the ID is not a TUPC
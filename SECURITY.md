# Security Policy – Keylogger

## Supported Versions

The Keylogger currently supports the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## System Requirements

- **Operating System**: Windows 7/8/10/11  
- **Python**: 3.4 or higher  
- **Required Libraries**:  
  - requests==2.31.0  
  - pynput==1.7.6  
  - psutil==5.9.5  

## Security Warnings

1. **Intended Use**  
   This Keylogger application is designed strictly for educational and testing purposes on devices that you own. Using it without the end user’s consent may violate local laws.  

2. **Information Protection**  
   - This project uses a Telegram Bot to transmit data.  
   - Bot token and chat ID should be replaced before deployment.  
   - It should not be used in critical environments or on systems containing sensitive information.  

3. **Security Risks**  
   - The bot token is stored in plain text within the source code.  
   - Collected information includes keystrokes, username, system information, and local IP address.  
   - No end-to-end encryption is applied to transmitted data.  

## Reporting Vulnerabilities

If you discover a security vulnerability in this application, please follow these steps:

1. **Do not disclose the vulnerability publicly** until it has been patched.  
2. Report it directly to the developer via email or private message.  
3. Provide a detailed description of the vulnerability and how it can be reproduced.  
4. If possible, suggest a fix or mitigation.  

Reports will be reviewed within **7 business days**. Status updates and resolution progress will be communicated.  

## Compliance Notice

Use of this application must comply with local privacy and data protection laws. Users are fully responsible for ensuring that their use aligns with applicable regulations.  

## Disabling Default Security Features

If necessary, you can disable data transmission via Telegram by modifying the source code.  
However, this is **not recommended** as the feature is intended for monitoring and tracking purposes.

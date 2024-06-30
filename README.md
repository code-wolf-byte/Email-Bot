# Email Listener and Sender Bot

## Overview

This project consists of a Discord bot that listens to incoming emails, processes them, and facilitates responses through Discord channels. It uses IMAP to fetch emails and SMTP to send responses. Additionally, it converts email bodies to images if they are HTML-based and manages attachments.

## Features

1. **Email Class**: Represents an email with attributes like sender, recipient, subject, body, attachments, etc.
2. **Email Listener**: Listens for new emails using IMAP and processes them.
3. **Email Sender**: Sends emails using SMTP.
4. **Discord Bot**: Integrates with Discord to create channels for each email and allows users to respond to emails through Discord.

## Setup

### Prerequisites

- Python 3.8+
- Discord bot token
- Gmail account with IMAP and SMTP access enabled

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/email-bot.git
    cd email-bot
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `config.json` file with the following content:
    ```json
    {
        "email": "your-email@gmail.com",
        "password": "your-email-password",
        "token": "your-discord-bot-token",
        "guild_id": "your-discord-guild-id"
    }
    ```

### Running the Bot

1. Start the Discord bot:
    ```bash
    python bot.py
    ```

## Usage

### Email Class

- **Attributes**:
  - `sender`: Email sender address.
  - `recipient`: Email recipient address.
  - `subject`: Email subject.
  - `body`: Email body content.
  - `attachments`: List of attachments.
  - `channel`: Associated Discord channel.
  - `id`: Unique identifier for the email.
  - `response`: Response to the email.
  - `responseFiles`: Files attached in the response.
  - `responseSubject`: Subject of the response.

### Email Listener

- **Methods**:
  - `__init__(username, password)`: Initializes the listener with email credentials.
  - `setupBot()`: Sets up the bot.
  - `isSetup()`: Checks if the bot is set up.
  - `parse_email(msg)`: Parses an email message.
  - `listen()`: Listens for new emails.
  - `removeASCII(text)`: Removes ASCII characters from the text.

### Email Sender

- **Methods**:
  - `__init__(email, password)`: Initializes the sender with email credentials.
  - `send_email(recipient, subject, body, attachments)`: Sends an email.

### Discord Bot

- **Commands**:
  - `setup`: Sets up the email listener.
  - `prune`: Deletes all channels in the guild.
  - `confirm`: Confirms the email response.
  - `send`: Sends the confirmed email response.
  - `getmessages`: Prints the last 20 messages in the channel.

## Additional Utilities

- **Utils**: Contains utility functions like checking if text is HTML and converting text to PNG images.

## Dependencies

- `uuid`
- `imaplib`
- `smtplib`
- `email`
- `os`
- `discord`
- `json`
- `asyncio`
- `requests`
- `html2image`
- `PIL`
- `beautifulsoup4`

## License

This project is licensed under the MIT License.

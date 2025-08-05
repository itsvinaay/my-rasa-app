# Rasa Chatbot with Coolify Deployment

This is a complete Rasa chatbot project configured for deployment on VPS using Coolify.

## Features

- **Natural Language Understanding**: Handles greetings, appointments, banking queries, weather, and more
- **Custom Actions**: Database integration, OpenAI integration, appointment booking
- **PostgreSQL Integration**: Stores conversation data and appointments
- **Docker Support**: Fully containerized for easy deployment
- **Coolify Ready**: Pre-configured for Coolify deployment

## Project Structure

```
├── config.yml              # Rasa NLU and Core configuration
├── domain.yml              # Bot domain (intents, entities, responses)
├── data/
│   ├── nlu.yml             # Training data for NLU
│   ├── rules.yml           # Conversation rules
│   └── stories.yml         # Training stories
├── actions/
│   ├── actions.py          # Custom actions
│   ├── Dockerfile          # Action server Docker configuration
│   └── requirements-actions.txt
├── endpoints.yml           # External service endpoints
├── credentials.yml         # Channel credentials
├── coolify.yaml           # Coolify deployment configuration
├── docker-compose.yml     # Local development setup
└── Dockerfile             # Rasa server Docker configuration
```

## Local Development

1. **Install Rasa**:
   ```bash
   pip install rasa
   ```

2. **Train the model**:
   ```bash
   rasa train
   ```

3. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

4. **Test the bot**:
   ```bash
   curl -X POST http://localhost:5005/webhooks/rest/webhook \
     -H "Content-Type: application/json" \
     -d '{"sender": "test", "message": "hello"}'
   ```

## Deployment on VPS with Coolify

### Prerequisites

1. **VPS with Coolify installed**
2. **Domain name** (optional but recommended)
3. **OpenAI API Key** (for AI-powered responses)

### Deployment Steps

1. **Clone/Upload Project**:
   ```bash
   git clone <your-repo> /path/to/project
   cd /path/to/project
   ```

2. **Configure Environment Variables in Coolify**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DB_URL`: PostgreSQL connection string (auto-configured)

3. **Deploy with Coolify**:
   - Import the project in Coolify dashboard
   - The `coolify.yaml` file will be automatically detected
   - Deploy the services

4. **Access Your Bot**:
   - Rasa API: `https://your-domain.com:5005`
   - Action Server: `https://your-domain.com:5055`

### Service Configuration

The `coolify.yaml` includes three services:

- **rasa-core**: Main Rasa server (port 5005)
- **action-server**: Custom actions server (port 5055)
- **postgres-db**: PostgreSQL database (port 5432, internal)

## API Endpoints

### Chat with Bot
```bash
POST /webhooks/rest/webhook
Content-Type: application/json

{
  "sender": "user123",
  "message": "Hello, I want to book an appointment"
}
```

### Health Check
```bash
GET /
```

### Model Information
```bash
GET /model
```

## Supported Intents

- **Greetings**: hello, hi, good morning
- **Appointments**: book appointment, cancel appointment
- **Banking**: check balance, transfer money
- **Information**: weather, time, help
- **Conversation**: mood expressions, affirmations

## Custom Actions

1. **action_book_appointment**: Books appointments in database
2. **action_cancel_appointment**: Cancels appointments
3. **action_check_balance**: Shows account balance
4. **action_transfer_money**: Handles money transfers
5. **action_get_weather**: Weather information
6. **action_get_time**: Current time
7. **action_ai_response**: OpenAI-powered responses

## Database Schema

The bot automatically creates necessary tables:

```sql
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(100),
    appointment_date VARCHAR(50),
    appointment_time VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for AI responses
- `DB_URL`: PostgreSQL connection string
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name

## Monitoring and Logs

Access logs through Coolify dashboard:
- Application logs
- Database logs
- Action server logs

## Scaling

The setup supports horizontal scaling:
- Multiple Rasa instances behind load balancer
- Shared PostgreSQL database
- Stateless action servers

## Security

- Environment variables for sensitive data
- Database connection encryption
- CORS configuration for web integration
- Input validation in custom actions

## Troubleshooting

1. **Model Training Issues**:
   ```bash
   rasa train --debug
   ```

2. **Action Server Connection**:
   Check endpoints.yml configuration

3. **Database Connection**:
   Verify DB_URL environment variable

4. **OpenAI API Issues**:
   Check API key and quota

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

MIT License - see LICENSE file for details.
</btml:Action>
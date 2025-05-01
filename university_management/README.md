# University Management System

A comprehensive microservices-based university management system built with Python and Flask.

## Project Structure

The system is organized into multiple microservices, each handling a specific domain:

1. People Microservice
2. Academic Microservice
3. Student Records Microservice
4. Finance Microservice
5. Resources Microservice
6. Library Microservice
7. Accommodation Microservice
8. Transportation Microservice
9. HR Microservice
10. Admissions Microservice
11. Events Microservice
12. Communication Microservice
13. Security Microservice
14. IT Support Microservice
15. Alumni Microservice
16. Research Microservice
17. Governance Microservice
18. Health Microservice
19. Career Microservice
20. Analytics Microservice
21. Sustainability Microservice
22. International Office Microservice
23. Parent Portal Microservice

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///people.db
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
flask run
```

## API Documentation

Each microservice exposes a RESTful API. Detailed API documentation is available in the respective service directories.

## Security

- JWT-based authentication
- Role-based access control
- Data encryption for sensitive information
- Audit logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
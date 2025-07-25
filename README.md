# PharmacyGenius Search API

A powerful drug search API using GPT-4o Search Preview to get real-time, comprehensive drug information from authoritative web sources.

## 🌟 Features

- **Real-time Web Search**: Uses GPT-4o Search Preview for up-to-date information
- **Comprehensive Drug Profiles**: Get detailed drug information including:
  - Basic information (name, classification, brand names)
  - Medical information (indications, mechanism of action)
  - Dosage guidelines
  - Safety information (side effects, contraindications)
  - Drug interactions
  - Regulatory status and formulations
- **Authoritative Sources**: Information from FDA, EMA, PubMed, and medical literature
- **RESTful API**: Clean, well-documented endpoints
- **Swagger Documentation**: Interactive API documentation
- **Postman Collection**: Ready-to-use test collection

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository and navigate to APIs folder
cd PharmacyGenius/apis

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Set your OpenAI API key:

**Windows:**
```cmd
set OPENAI_API_KEY=your_openai_api_key_here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

**Or create a `.env` file:**
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Start the API

**Option A: Using the startup script (recommended)**
```bash
python start_api.py
```

**Option B: Direct uvicorn command**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the API

- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/

## 📚 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message and API info |
| GET | `/health` | Health check and OpenAI connectivity |
| GET | `/info` | Detailed API information and capabilities |

### Search Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/search/drug` | Main drug search with detailed options |
| GET | `/search/quick` | Quick drug search with query parameter |

## 🔍 Usage Examples

### Basic Drug Search

```bash
curl -X POST "http://localhost:8000/search/drug" \
     -H "Content-Type: application/json" \
     -d '{
       "drug_name": "aspirin",
       "include_dosage": true,
       "include_side_effects": true,
       "include_interactions": false
     }'
```

### Quick Search (GET)

```bash
curl "http://localhost:8000/search/quick?drug_name=ibuprofen"
```

### Comprehensive Search with Interactions

```bash
curl -X POST "http://localhost:8000/search/drug" \
     -H "Content-Type: application/json" \
     -d '{
       "drug_name": "lisinopril",
       "include_dosage": true,
       "include_side_effects": true,
       "include_interactions": true
     }'
```

## 📋 Request/Response Format

### Request Schema

```json
{
  "drug_name": "string",           // Required: Name of the drug
  "include_dosage": true,          // Optional: Include dosage info
  "include_side_effects": true,    // Optional: Include side effects
  "include_interactions": false    // Optional: Include drug interactions
}
```

### Response Schema

```json
{
  "success": true,
  "data": {
    "drug_name": "aspirin",
    "drug_information": "Detailed drug information...",
    "search_options": {
      "include_dosage": true,
      "include_side_effects": true,
      "include_interactions": false
    },
    "timestamp": "2024-01-01T12:00:00"
  },
  "message": "Successfully retrieved information for 'aspirin'",
  "processing_time": 3.45
}
```

## 🧪 Testing

### Using Postman

1. Import the collection: `PharmacyGenius_Search_API.postman_collection.json`
2. The collection includes:
   - API information endpoints
   - Drug search examples
   - Test cases for common medications
   - Error testing scenarios

### Using Swagger UI

1. Go to http://localhost:8000/docs
2. Try out any endpoint directly in the browser
3. View request/response schemas and examples

### Manual Testing

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Basic Search:**
```bash
curl -X POST "http://localhost:8000/search/drug" \
     -H "Content-Type: application/json" \
     -d '{"drug_name": "acetaminophen"}'
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | None |
| `API_HOST` | API host address | 0.0.0.0 |
| `API_PORT` | API port | 8000 |
| `ENVIRONMENT` | Environment mode | development |

### API Settings

The API is configured with:
- CORS enabled for all origins (configure for production)
- Request timeout: 30 seconds
- Low temperature (0.1) for factual responses
- Maximum 2000 tokens per response

## 📊 Data Sources

The API searches information from:
- **FDA** (Food and Drug Administration)
- **EMA** (European Medicines Agency)
- **PubMed** medical literature
- **Official drug labels**
- **Medical textbooks and databases**

## ⚠️ Important Notes

### Rate Limits
- Subject to OpenAI API rate limits
- Recommended: 60 requests per minute for GPT-4o

### Data Accuracy
- Information is sourced from authoritative medical sources
- Always verify drug information with official sources
- This API is for informational purposes only

### Security
- Configure CORS properly for production
- Protect your OpenAI API key
- Consider implementing authentication for production use

## 🛠️ Development

### Project Structure

```
apis/
├── main.py                                    # Main FastAPI application
├── requirements.txt                           # Python dependencies
├── start_api.py                              # Startup script
├── PharmacyGenius_Search_API.postman_collection.json  # Postman collection
└── README.md                                 # This file
```

### Adding Features

1. **New Endpoints**: Add to `main.py`
2. **New Models**: Add Pydantic models for request/response
3. **Testing**: Update Postman collection
4. **Documentation**: Update docstrings and this README

### Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **OpenAI**: GPT-4o integration
- **Pydantic**: Data validation
- **python-dotenv**: Environment management

## 🐛 Troubleshooting

### Common Issues

**"OpenAI client not configured"**
- Set your `OPENAI_API_KEY` environment variable
- Verify the API key is valid

**"Failed to search for drug information"**
- Check your internet connection
- Verify OpenAI API key has sufficient credits
- Check API rate limits

**Import errors**
- Install requirements: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### Debug Mode

Run with debug logging:
```bash
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
import uvicorn
uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
"
```

## 📞 Support

For issues and questions:
1. Check the [troubleshooting section](#-troubleshooting)
2. Review the API documentation at `/docs`
3. Test with the provided Postman collection
4. Check OpenAI API status and rate limits

## 📄 License

MIT License - See project root for details.

---

**Ready to search for drug information!** 🔬💊 
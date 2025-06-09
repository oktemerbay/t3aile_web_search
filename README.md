# T3AI Projesi - Web Search API Entegrasyonu

Bu dosya, T3AI projesi kapsamında kullanılan Web Search API sağlayıcılarını ve projeyi çalıştırmak için gerekli `.env` dosyası parametrelerini içermektedir.

## Entegre Edilen Web Search API Sağlayıcıları

T3AI içerisinde aşağıdaki web search API sağlayıcıları desteklenmektedir:

* **Brave Search API**
* **SearXNG (Self-hosted)**
* **Contextual Web API**
* **Google Custom Search API**
* **SerpAPI**
* **Serper.dev**

---

## .env Dosyası İçeriği

Uygulamanın çalışabilmesi için proje dizinine aşağıdaki içeriğe sahip bir `.env` dosyası eklenmelidir:

```env
# Brave Search API Token
BRAVE_SEARCH_TOKEN=***************

# Uygulamanın arama sonuçlarını çıktığı klasör
MAIN_OPERATION_PATH=/path/to/local/

# SearXNG Self-hosted arama servisi adresi
SEARXNG_HOST_URL=http://localhost:8080/search

# Contextual Web API Anahtarı
CONTEXTUAL_WEB_API_KEY=***************

# Google Custom Search Ayarları
GOOGLE_CUSTOM_SEARCH_KEY=***************
GOOGLE_CUSTOM_SEARCH_CX=***************

# SerpAPI Anahtarı
SERP_API_API_KEY=***************

# Serper.dev Anahtarı
SERPER_DEV_API_KEY=***************

#Facebook Faiss RAG yapısının kullanılıp kullanılmayacağı ; False ise kullanılmaz , True ise devreye girer
IS_USE_FAISS=False
```

> 📌 **Not:** Yukarıdaki değerlerin her biri ilgili servis sağlayıcıdan alınmalıdır. Güvenlik açısından gerçek anahtarlar paylaşılmamalı ve `.env` dosyası `.gitignore` içine eklenmelidir.

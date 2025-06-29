# T3 AI'LE Web Search Pipeline

## 🧠 Proje Hakkında

**T3 AI'LE**, Türkiye'nin büyük dil modeli (LLM) oluşturma vizyonu kapsamında geliştirilmiş açık kaynaklı bir projedir. Bu proje, kullanıcılardan alınan doğal dil sorgularını web üzerinden aratıp, sonuçları büyük dil modeli ile işleyerek zenginleştirilmiş yanıtlar üretir. 

Ana hedefimiz, Türkçe dilinde güçlü bilgi tabanı oluşturarak Türkiye'ye ait özgün ve güncel içerikleri, yapay zeka destekli bir pipeline ile kullanıcıya sunmaktır.

---

## 🔧 Özellikler

✅ Kullanıcıdan doğal dil sorgusu alma  
✅ Seçilebilir Search API modülleri  
✅ Search API üzerinden web araması yapma  
✅ Sonuçları büyük dil modeli (LLM) ile işleyip anlamlı cevaplar üretme  
✅ Modüler ve genişletilebilir mimari  
✅ Tamamen açık kaynak ve topluluk katkısına açık yapı

---

## Entegre Edilen Web Search API Sağlayıcıları

T3AI içerisinde aşağıdaki web search API sağlayıcıları desteklenmektedir:

* **Brave Search API**
* **SearXNG (Self-hosted)**
* **Contextual Web API**
* **Google Custom Search API**
* **SerpAPI**
* **Serper.dev**

---

Projeyi çalıştırmak için gerekli `.env` dosyası parametrelerini aşağıda paylaşıyorum.

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

## 🗂️ Proje Yapısı

├── common/__
│ ├── constants.py__
│ ├── common.py__
│ └── LLMEvaluator.py__
├── search_modules/__
│ ├── BraveSearchAPI.py
│ ├── ContextualWebAPI.py
│ ├── GoogleCustomSearch.py
│ ├── Searxng.py
│ ├── SerpAPI.py
│ ├── SerpAPI.py
│ └── SerperDev.py
├── search_module.py
├── requirements.txt
└── README.md

- **common/**: Ortak fonksiyonlar, sabitler ve LLM evaluator modülü  
- **search_modules/**: Farklı arama motorları için modüller  
- **search_module.py**: Arama motoru seçim ve dispatch mekanizması


> 📌 **Not:** Yukarıdaki değerlerin her biri ilgili servis sağlayıcıdan alınmalıdır. Güvenlik açısından gerçek anahtarlar paylaşılmamalı ve `.env` dosyası `.gitignore` içine eklenmelidir.

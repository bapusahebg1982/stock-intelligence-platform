from database.db import SessionLocal
from database.models import Stock
from services.market_scraper import scrape_sp500, scrape_nifty500


def refresh_universe():

    db = SessionLocal()

    try:
        # clear old data
        db.query(Stock).delete()

        us_tickers = scrape_sp500()
        in_tickers = scrape_nifty500()

        # 🔥 fallback if scraping fails
        if not us_tickers:
            us_tickers = ["AAPL","MSFT","NVDA","AMZN"]

        if not in_tickers:
            in_tickers = ["RELIANCE.NS","TCS.NS","INFY.NS"]

        for t in us_tickers:
            db.add(Stock(ticker=t, market="US"))

        for t in in_tickers:
            db.add(Stock(ticker=t, market="IN"))

        db.commit()

        return {
            "US": len(us_tickers),
            "IN": len(in_tickers)
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()


def get_universe(market="US", limit=100):

    db = SessionLocal()

    try:
        stocks = db.query(Stock).filter(Stock.market == market).limit(limit).all()
        return [s.ticker for s in stocks]

    except:
        return []

    finally:
        db.close()

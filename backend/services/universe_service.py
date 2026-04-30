from database.db import SessionLocal
from database.models import Stock
from services.market_scraper import scrape_sp500, scrape_nifty500


def refresh_universe():

    db = SessionLocal()

    # clear old
    db.query(Stock).delete()

    # fetch new
    us_tickers = scrape_sp500()
    in_tickers = scrape_nifty500()

    for t in us_tickers:
        db.add(Stock(ticker=t, market="US"))

    for t in in_tickers:
        db.add(Stock(ticker=t, market="IN"))

    db.commit()
    db.close()

    return {
        "US": len(us_tickers),
        "IN": len(in_tickers)
    }


def get_universe(market="US", limit=100):

    db = SessionLocal()

    stocks = db.query(Stock).filter(Stock.market == market).limit(limit).all()

    db.close()

    return [s.ticker for s in stocks]

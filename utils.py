import requests


def get_max_value(data):
    # getting max value from reviews data
    reviews_number = {
        "ratings_count": data['ratings_count'],
        "reviews_count": data['reviews_count'],
        "text_reviews_count": data['text_reviews_count'],
        "work_ratings_count": data['work_ratings_count'],
        "work_reviews_count": data['work_reviews_count']
    }
    return max(reviews_number.values())


def get_percentages(data):
    # converting reviews data to percentages to facilitate styling
    # reviews card plot
    max_value = get_max_value(data) + 2
    percentages = {
        "ratings_count": (data['ratings_count'] / max_value) * 100,
        "reviews_count": (data['reviews_count'] / max_value) * 100,
        "text_reviews_count": (data['text_reviews_count'] / max_value) * 100,
        "work_ratings_count": (data['work_ratings_count'] / max_value) * 100,
        "work_reviews_count": (data['work_reviews_count'] / max_value) * 100
    }
    return percentages


def format_reviews_data(data):
    data = data.json()['books'][0]
    percentages = get_percentages(data)
    sorted_data = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
    titles = {
        "ratings_count": "Ratings",
        "reviews_count": "Reviews",
        "text_reviews_count": "Text reviews",
        "work_ratings_count": "Work ratings",
        "work_reviews_count": "Work reviews"
    }
    formatted_number = []
    for key, value in sorted_data:
        __data = {
            "title": titles[key],
            "percentage": f"{value:.5g}%",
            "total": data[key]
        }
        formatted_number.append(__data)

    return {
        "average_rating": data['average_rating'],
        "ratings_count": data['ratings_count'],
        "reviews_numbers": formatted_number
    }


def validate_reviews(reviews, book_id, request, session):
    # check user has already reviews the book
    review = reviews.fetchone(query="WHERE user_id = :user_id AND book_id = :book_id",
                              value={"user_id": session['user_id'], "book_id": book_id})

    errors = [
        {"error": "You are already reviewed this book."},
        {"error": "Comment is required"}
    ]
    return errors[0] if review else errors[1] if not request.json.get('comment') else True


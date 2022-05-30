def average_book_rating(rating_list):
    # print(rating_list)
    if not rating_list:
        return 0
    return round(sum(rating_list)/len(rating_list))
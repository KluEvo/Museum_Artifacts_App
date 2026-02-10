import os
import requests

class main:
    def __init__(self):
        self.running = True

    def start(self):
        print('Welcome to the museum app. Type \'help\' for a list of commands')
        while self.running:
            cmd = input('>>>').strip()
            self.handle_command(cmd)
    
    # TODO: Edit all cases for current project
    def handle_command(self, cmd):
        match cmd:
            case 'exit':
                self.running = False
                print("goodbye!")
            case 'getAllRecords':
                self.get_all_records()
            case 'addBook':
                self.add_book()
            case 'findByName':
                self.find_book_by_name()
            case 'removeBook':
                self.remove_book()
            case 'updateBook':
                self.update_book()
            case 'getAveragePrice':
                self.get_average_price()
            case 'getTopBooks':
                self.get_top_books()
            case 'getValueScores':
                self.get_value_scores()
            case 'medianPriceByGenre':
                self.get_median_price_by_genre()
            case 'priceSD':
                self.get_price_std_dev()
            case 'priceCorr':
                self.get_price_correlation()
            case 'pricePercent':
                self.get_price_percentiles()
            case 'ratingHist':
                self.get_rating_histogram()
            case 'genrePop2026':
                self.get_most_popular_genre_2026()
            case 'checkIn':
                self.check_in_book()
            case 'checkOut':
                self.check_out_book()
            case 'checkoutHist':
                self.get_check_out_history()
            case 'getJoke':
                self.get_joke()
            case 'help':
                print("Commands:")
                print("addBook, removeBook, updateBook, getAllRecords, findByName, getJoke, help, exit")
                print("getAveragePrice, getTopBooks, getValueScores, medianPriceByGenre, genrePop2026")
                print("priceSD, pricePercent, priceCorr, ratingHist")
                print("checkIn, checkOut, checkoutHist")
            case _:
                print("No valid command detected")


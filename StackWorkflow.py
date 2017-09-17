from bs4 import BeautifulSoup as bs
import requests

def get_input(): #Takes a string explaining the rules of the input and asks the user to input a response
    search_term=input("What would you like help with: ")
    return search_term

class ask():
    def __init__(self):
        self.so_url="https://stackoverflow.com"
        self.search_url="https://stackoverflow.com/search?tab=votes&q=%5bpython%5d"
        self.execute()

    def make_search_url(self,search_term): #Taking a search term as input, turns search_url into a viable url
        keyword=search_term.replace(" ","%20")
        url=self.search_url+"%20"+keyword
        return url

    def get_page(self, url): #Takes a url and returns the BeautifulSoup formatted HTML source code
        page=requests.get(url)
        text=page.text #Unformatted HTML
        content=bs(text, "html.parser")
        return content

    def get_useable_answers(self, search_summary): #Given a search_summary, returns only links with positive answers
        revised_summary={}
        if len(search_summary)>0:
            for page in search_summary:
                if page>0:
                    revised_summary[page]=search_summary[page]
            if len(revised_summary)<0:
                print("There are no reliable answers.")
                raise SystemExit
            else:
                return revised_summary
        else:
            print("There are no reliable answers.")
            raise SystemExit

    def condense_questions(self, url): #Extracts the useful data from all questions on the page and stores them in search_summary
        content=self.get_page(url)
        search_summary = {}  # Key is the number of votes on a question, value is a list with the url and question title
        questions=content.find_all(class_="question-summary search-result")
        for q in questions:
            num_votes=q.find_all(class_="vote-count-post")
            href = q.find_all("a", href=True)
            href = href[0]
            title = href.string.replace("\r\n", "").rstrip()[11:]
            search_summary[int(num_votes[0].string)]=[str(href["href"]), title]
        return self.get_useable_answers(search_summary)

    def make_answer_url(self, search_summary,index=0): #Creates a working url for the answers page.
        votes=sorted(search_summary.keys(), reverse=True)
        votes=votes[int(index)-1:]
        extension=(search_summary[max(votes)])[0]
        url=self.so_url+extension
        return url

    def get_answer(self, url): #Returns the top answer for the given page url
        content=self.get_page(url)
        answer=[]
        answer_content=(content.find_all(class_="answercell"))[0]
        return (answer_content.find_all(class_="post-text"))[0].get_text()


    def execute(self):
        search_term=get_input()
        url=self.make_search_url(search_term)
        search_summary=self.condense_questions(url)
        count=1
        for i in search_summary:
            print(str(count)+". "+str((search_summary[i])[1]))
            count+=1
        done = False
        while True:
            index=input("Which of these questions sounds the most like your yours? ")
            answer=self.get_answer(self.make_answer_url(search_summary, index))
            print(answer)
            satisfied = input("Would you like to see the other questions again? [Y/N]")
            if satisfied.lower() == "n":
                break
            else:
                for i in search_summary:
                    print(str(count)+". "+str((search_summary[i])[1]))
                    count+=1
                
                
                




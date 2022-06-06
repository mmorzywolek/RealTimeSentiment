from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class AnalizeAppend:

    def __init__(self, docx: str) -> dict:
        self.docx = docx

    def analyze_token_sentiment(self):
        analyzer = SentimentIntensityAnalyzer()
        pos_list = []
        neg_list = []
        neu_list = []
        for i in self.docx.split():
            res = analyzer.polarity_scores(i)['compound']
        if res > 0.1:
            pos_list.append('positive')
            # pos_list.append(res)

        elif res <= -0.1:
            neg_list.append('negative')
            # neg_list.append(res)
        else:
            neu_list.append('neutral')

        result = {'sentence': self.docx, 'positives': pos_list, 'negatives': neg_list, 'neutral': neu_list}
        return result
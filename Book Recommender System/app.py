from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
PT = pickle.load(open('PT.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
S_Score = pickle.load(open('S_Score.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values),
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(PT.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(S_Score[index])), key=lambda x: x[1], reverse=True)[1:10]  # with enumerate we can see the item's index with their distance and sorted using similarity score

    data = []
    for i in similar_items:
        item = []

        temp_df = books[books['Book-Title'] == PT.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))

        data.append(item)

        print(data)

    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)


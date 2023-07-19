from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from urllib.parse import urlparse, unquote
import plotly.express as px
from collections import Counter
import ast

app = Flask(__name__)

app.config['SECRET_KEY'] = 'parabah'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0000@localhost/data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, nullable=False, default=3)

    def __repr__(self):
        return f"<Utilisateur {self.nom} {self.prenom}>"

def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8', sep=';')
        print(df.head(4))
        return df
    except pd.errors.ParserError as e:
        error_msg = "Erreur lors de la lecture du fichier CSV : {}".format(str(e))
        print(error_msg)
        return None

def extract_product_name_from_url(url):
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)  # Décodage de l'URL si nécessaire
    segments = path.split('/')  # Séparation des segments de l'URL
    product_name = segments[-2]  # Récupération du dernier segment correspondant au nom du produit
    return product_name

def create_pie_chart(df, product_name):
    filtered_df = df[df['review_url_src'].str.contains(product_name, case=False)]
    sentiment_counts = filtered_df['sentiment_category'].value_counts()
    labels = sentiment_counts.index
    values = sentiment_counts.values
    review_count = len(filtered_df)

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title_text=f"Produit : {product_name} ({review_count} revues)")

    plot_div = fig.to_html(full_html=False)

    return plot_div

def create_star_distribution_histogram(df, product_name):
    filtered_df = df[df['review_url_src'].str.contains(product_name, case=False)]
    fig = px.histogram(filtered_df, x='review_stars')
    fig.update_layout(title_text=f"Distribution des étoiles pour le produit : {product_name}")
    plot_div = fig.to_html(full_html=False)
    return plot_div

def create_keyword_frequency_bar_chart(df, product_name):
    filtered_df = df[df['review_url_src'].str.contains(product_name, case=False)]
    # Convert strings of lists to lists
    filtered_df["keywords"] = filtered_df["keywords"].apply(ast.literal_eval)
    # Flatten list of lists
    flat_keywords = [keyword for sublist in filtered_df.keywords for keyword in sublist]
    keyword_counts = Counter(flat_keywords)
    fig = px.bar(x=list(keyword_counts.keys()), y=list(keyword_counts.values()))
    fig.update_layout(title_text=f"Fréquence des mots-clés pour le produit : {product_name}")
    plot_div = fig.to_html(full_html=False)
    return plot_div

def create_review_time_series(df, product_name):
    filtered_df = df[df['review_url_src'].str.contains(product_name, case=False)]
    filtered_df['review_date'] = pd.to_datetime(filtered_df['review_date'])  # Convert review_date to datetime
    fig = px.line(filtered_df, x='review_date', y='review_stars')
    fig.update_layout(title_text=f"Série temporelle des étoiles pour le produit : {product_name}")
    plot_div = fig.to_html(full_html=False)
    return plot_div

def create_three_variable_bubble_chart(df, product_name):
    filtered_df = df[df['review_url_src'].str.contains(product_name, case=False)]
    fig = px.scatter(filtered_df, x='review_stars', y='sentiment_category', size='review_tup', color='review_verified')
    fig.update_layout(title_text=f"Diagramme à bulles pour le produit : {product_name}")
    plot_div = fig.to_html(full_html=False)
    return plot_div

@app.route('/home', methods=['GET', 'POST'])
def home():
    # Vérifier si l'utilisateur est connecté et si c'est un administrateur ou un utilisateur normal
    if 'user_id' not in session or session['role_id'] not in [1, 2]:
        return redirect(url_for('login'))

    df = read_csv_file("output_with_sentiments_keywords.csv")
    if df is None:
        error_msg = "Erreur lors de la lecture du fichier CSV. Veuillez vérifier le format du fichier."
        return render_template('home.html', error_msg=error_msg)

    # Extract unique product names
    product_names = df['review_url_src'].apply(extract_product_name_from_url).unique()

    if request.method == 'POST':
        selected_product = request.form.get('product')
        try:
            pie_chart_div = create_pie_chart(df, selected_product)
            histogram_div = create_star_distribution_histogram(df, selected_product)
            bar_chart_div = create_keyword_frequency_bar_chart(df, selected_product)
            time_series_div = create_review_time_series(df, selected_product)
            bubble_chart_div = create_three_variable_bubble_chart(df, selected_product)
        except ValueError as e:
            error_msg = "Erreur lors de la création du graphique : {}".format(str(e))
            return render_template('home.html', error_msg=error_msg, product_names=product_names)

        return render_template('home.html', pie_chart_div=pie_chart_div, histogram_div=histogram_div, bar_chart_div=bar_chart_div, time_series_div=time_series_div, bubble_chart_div=bubble_chart_div, product_names=product_names)

    return render_template('home.html', product_names=product_names)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        password = request.form.get('mot_de_passe')
        confirm_password = request.form.get('confirm_password')

        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            error_msg = 'Les mots de passe ne correspondent pas'
            return render_template('register.html', error_msg=error_msg)

        # Vérifier si l'utilisateur existe déjà dans la base de données
        existing_user = Utilisateur.query.filter_by(email=email).first()
        if existing_user:
            error_msg = 'Un utilisateur avec cet email existe déjà'
            return render_template('register.html', error_msg=error_msg)

        # Créer un nouvel utilisateur
        hashed_password = generate_password_hash(password)
        utilisateur = Utilisateur(nom=nom, prenom=prenom, email=email, mot_de_passe=hashed_password)

        # Enregistrer l'utilisateur dans la base de données
        db.session.add(utilisateur)
        db.session.commit()

        # Redirection vers la page de connexion
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    # Supprimer les informations de l'utilisateur de la session
    session.pop('user_id', None)
    # Rediriger l'utilisateur vers la page de connexion
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        utilisateur = Utilisateur.query.filter_by(email=email).first()
        if utilisateur and check_password_hash(utilisateur.mot_de_passe, password):
            # Ajouter les informations de l'utilisateur à la session
            session['user_id'] = utilisateur.id
            session['role_id'] = utilisateur.role_id

            # Vérifier le rôle de l'utilisateur
            if utilisateur.role_id in [1, 2]:
                return redirect(url_for('home'))  # Redirection vers la page home
            else:
                error_msg = "Vous n'avez pas les droits d'accès à l'application"
                return render_template('login.html', error_msg=error_msg)
        else:
            error_msg = 'Identifiants de connexion invalides'
            return render_template('login.html', error_msg=error_msg)

    return render_template('login.html')

@app.route('/manage_access', methods=['GET', 'POST'])
def manage_access():
    # Vérifier si l'utilisateur est connecté et si c'est un administrateur
    if 'user_id' not in session or session['role_id'] != 1:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Récupérer les informations du formulaire
        user_id = request.form.get('user_id')
        new_role = request.form.get('new_role')

        # Trouver l'utilisateur correspondant
        user = Utilisateur.query.get(user_id)
        if user:
            # Modifier le rôle de l'utilisateur
            user.role_id = new_role
            db.session.commit()

    # Récupérer tous les utilisateurs pour les afficher
    users = Utilisateur.query.all()

    return render_template('manage_access.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)

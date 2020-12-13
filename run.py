from goc import app

if __name__ == '__main__':
    app.run(debug=True)
    app.run("0.0.0.0", port=8000)
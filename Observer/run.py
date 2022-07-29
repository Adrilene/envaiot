from project import app


if __name__ == "__main__":
    port = 4001
    print(f'Running Observer port:{port}')
    app.run(port=port, debug=True)

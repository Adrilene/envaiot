from project import app


if __name__ == "__main__":
    port = 4002
    print(f'Running Effector port:{port} \n')
    app.run(port=port, debug=True)

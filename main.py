# _*_coding:utf-8_*_
# Created by #Suyghur, on 2020-06-14.
# Copyright (c) 2020 3KWan.
# Description :
from fcore.app import create_app
from fcore.api.view import create_view

app = create_app()
create_view(app)

if __name__ == '__main__':
    app.run()

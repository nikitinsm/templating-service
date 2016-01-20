### Examples 

template:

**test.html**

    <html>
        <head></head>
        <body>
            <h1>
                {{ test|default("{{ test }} 
                also you can try iterable in {{ test2 }}") }}
            </h1>
            {% if test2 %}
            <ul>
                {% for item in test2 %}
                    <li>{{ item }}</li>
                {% endfor %}
            </ul>
            {% endif %}
        </body>
    </html>

**http GET: test.html**
    
    <html>
        <head></head>
        <body>
            <h1>{{ test }} also you can try iterable in {{ test2 }}</h1>
        </body>
    </html>
    <!--0.000721-->
    
**http POST: test.html with data:**
    
```
#!json
{ 
    "test": "2",
    "test2": [1, 2, 3]
}
```
    
result:

    <html>
        <head></head>
        <body>
            <h1>2</h1>
            <ul>
                <li>1</li>
                <li>2</li>
                <li>3</li>
            </ul>
        </body>
    </html>
    <!--0.000544-->
    
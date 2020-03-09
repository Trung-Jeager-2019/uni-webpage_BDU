// show quotes on startup

(function() {
    var quotes = [
    {q: 'I am very thankful to have taken this course -- it gave me a solid base from which to teach.', a: 'Alison, TESOL Certificate' },
    {q: 'I learned so many things and now have the confidence to study a university course in English.', a:'Seng, IEP Advanced'},
    {q: 'I study English in class and it is very interesting. I really like studying here with my new friends.', a:'Souaney, IEP Intermediate'},
    {q: 'This class helped my English get better. I really like it. It is fun and helps me improve my English.', a:'Sal Lao Khay Sue, IEP Intermediate'},
    {q: 'My TESOL training has given me invaluable resources for working with my students.', a:'Katie, TESOL Certificate'}
    ];
    var randQuotes = function (quotes) {
        var i = Math.floor(Math.random()*quotes.length);
        document.getElementById('randomquote').innerHTML = (quotes[i].q);
        document.getElementById('author').innerHTML = (quotes[i].a);
    };
    randQuotes(quotes);
    setInterval(function() {
        randQuotes(quotes);
    }, 5000);
})();

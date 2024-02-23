var refreshRate = Number(document.currentScript.getAttribute('data-refreshrate'));
var currency = document.currentScript.getAttribute('data-currency')
var ticker = document.currentScript.getAttribute('data-ticker')

function price_format(price) {
    if (price >999){
        return Number(price).toLocaleString("en-US");
    }else{
        return price;
    }
};

function fetchdata(){
    fetch('https://api3.binance.com/api/v3/ticker/price')
    .then(response => response.json())
    .then(data => {
        const Data = data.find(item => item.symbol == ticker.toUpperCase()+currency.toUpperCase());
        if (Data) {
        $("#price").html(price_format(Data.price.replace(/\.?0+$/, "")));
        } else {
            $("#price").html("NaN");
            $("#img").attr("src", 'https://cdn0.iconfinder.com/data/icons/shift-interfaces/32/Error-512.png')
        }
        }
    )
}


function Refresh() {
    fetchdata()
    setTimeout(Refresh, refreshRate*1000);
}
Refresh();


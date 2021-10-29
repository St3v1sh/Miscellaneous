/**
 * This code is a WIP. It will turn the first server in your Discord server
 * list into a cookie clicker minigame.
 * 
 * @author  sky3947@rit.edu
 * @since   10.29.2021
 */

var counter = 0;
var clickButton = document.querySelector('[aria-label="Servers"]').childNodes[0];

var pageContent = document.getElementsByClassName("content-98HsJk")[0];

var gameContent = document.createElement("DIV");
gameContent.setAttribute("style", "min-width: 200px; max-width: 200px; word-break: break-all; border-left: #2f3136 solid 1px; color: var(--header-primary); display: none;");
pageContent.prepend(gameContent);

var cookieCountContainer = document.createElement("DIV");
cookieCountContainer.setAttribute("style", "padding: 15px 0px; border-bottom: #2f3136 solid 1px;");
var cookieCount = document.createElement("H1");
cookieCount.setAttribute("style", "font-size: large; font-family: var(--font-display); text-align: center; margin: 0px 10px;");
cookieCountContainer.append(cookieCount);
gameContent.append(cookieCountContainer);

function timeoutfn(id, t, d) {
    setTimeout(function() {
        var element = document.getElementById(id);
        if(t >= 20) {
            element.parentNode.removeChild(element);
        } else {
            element.setAttribute("style", "color: white; position: absolute; font-weight: bold; top: "+(16-2*t)+"px; left: "+(20+d)+"px;");
            timeoutfn(id, t+1, d);
        }
    }, 50);
}

const buttonsUpdate = () => {
    setTimeout(() => {
        var newClickButton = document.querySelector('[aria-label="Servers"]').childNodes[0];
        if (clickButton != newClickButton) {
            clickButton.removeEventListener("click", cookieclick);
            newClickButton.addEventListener("click", cookieclick);
            clickButton = newClickButton;
        }
        buttonsUpdate();
    }, 1000);
};

function cookieclick() {
    var plus = document.createElement("DIV");
    var textnode = document.createTextNode("+1");
    plus.append(textnode);
    d = Math.random()*12;
    plus.setAttribute("style", "color: white; position: absolute; font-weight: bold; top: 16px; left: "+(20+d)+"px;");
    plus.setAttribute("id", "clicked"+(++counter));
    cookieCount.innerHTML = `🍪 ${counter}`;
    gameContent.style.display = "block";
    clickButton.appendChild(plus);
    timeoutfn("clicked"+counter, 0, d);
}

buttonsUpdate();
clickButton.addEventListener("click", cookieclick);

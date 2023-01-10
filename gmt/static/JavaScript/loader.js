//Adding a delay of 2 seconds to fadeout the loader
const loaderText = ["Loading Good Morning Tech", "Coming up, Good Morning Tech!", "Good Morning Tech, we're almost there!", "Loading your favorite newsletter website!"]
//Randomizing the loader text
const randomText = loaderText[Math.floor(Math.random() * loaderText.length)]
//Adding the random text to the loader
$(".loader-text").text(randomText)
//Fading out the loader
setTimeout(() => {
    $(".loader-wrapper").fadeOut(750);
}, 1000); // 1.5 seconds 

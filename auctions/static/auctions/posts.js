function convertDateFormat(originalDate) {
    const date = new Date(originalDate);
    
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

let currently_loading = false;
let some_listing_left = true;
// Start with listing 1
let counter = 1;

// Load listings 3
const quantity = 3;

// When DOM loads, render the first 3 listings
document.addEventListener("DOMContentLoaded", () => {
    if (document.querySelector("#articlesContainer")){
        load();
    }
    if (document.querySelector("#showMore_btn")){
        document.querySelector("#showMore_btn").addEventListener("click", () => {
            load();
        });
    }
});


// Load next set of listings
function load(){
    // Set start and end listing numbers and update counter
    const start = counter-1;
    const end = start + quantity;
    counter = end + 1;

    // Get new listinga and add listings
    fetch(`/listing?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        if (data.length !== 0){
            some_listing_left = true;
            document.querySelector("#showMore_btn").style.display = "block";
            console.log("Loading more listings");
        }
        else{
            some_listing_left = false;
            document.querySelector("#showMore_btn").style.animationPlayState = 'running';
            document.querySelector("#showMore_btn").addEventListener("animationend", () => {
                document.querySelector("#showMore_btn").style.display = "none";
            });
            console.log("No more listings");
        }
        console.log(data);
        data.forEach(data_element => {
                add_listing(data_element);
        });
        currently_loading = false;
    })
    .catch(error => console.error("Error fetching data:", error));
}

function add_listing(listing_data){
    // Add listing to DOM
    document.querySelector('#articlesContainer').append(createListing(listing_data));
};

window.onscroll = () => {
    const windowHeight = window.innerHeight;
    const scrollY = window.scrollY;
    const documentHeight = document.body.offsetHeight;

    if ((window.innerHeight + window.scrollY + 2 >= document.body.offsetHeight) && !currently_loading && some_listing_left){
        currently_loading = true;
        console.log("End of the page...");
        load();
    }
}

function createListing(element){
    const article = document.createElement("article");
    const link = document.createElement("a");

    link.href = `${element['pk']}`;
    link.classList.add("text-decoration-none");
    article.appendChild(link);

    const rowDiv = document.createElement("div");
    rowDiv.classList.add("row", "mb-3");
    link.appendChild(rowDiv);

    const imgDiv = document.createElement("div");
    imgDiv.classList.add("col-md-2");
    rowDiv.appendChild(imgDiv);

    const listing_img = document.createElement("img");
    listing_img.src = "media/" + element["fields"]["image"];
    listing_img.alt = element["fields"]["title"];
    listing_img.classList.add("img-fluid", "rounded", "object-fit-contain");
    imgDiv.appendChild(listing_img);

    const infoDiv = document.createElement("div");
    infoDiv.classList.add("col-md-6", "d-flex", "flex-column");
    rowDiv.appendChild(infoDiv);

    const wrapTitle = document.createElement("div");
    wrapTitle.classList.add("row", "container");
    infoDiv.appendChild(wrapTitle);

    // To change - so it shows real waitlist
    const title = document.createElement("h3");
    title.innerHTML = element["fields"]["title"];
    wrapTitle.appendChild(title);
    if (element["fields"]["watch_list"].includes(element["logged_user"])){
        const watch_list = document.createElement("div");
        watch_list.classList.add("ml-auto", "mb-auto", "badge", "bg-secondary", "mt-auto");
        watch_list.id="white";
        watch_list.innerHTML = "watchlist";
         wrapTitle.appendChild(watch_list);
    }

    const priceInfo = document.createElement("h5");
    priceInfo.innerHTML = `Price: ${element["fields"]["price"]}`;
    infoDiv.appendChild(priceInfo);

    const postfixDiv = document.createElement("div");
    postfixDiv.classList.add("mt-auto", "row", "container");
    infoDiv.appendChild(postfixDiv);
    
    const userDiv = document.createElement("div");
    userDiv.innerHTML = `<i>Added by: ${element["fields"]["creator_name"]}</i>`;
    postfixDiv.appendChild(userDiv);

    const dateDiv = document.createElement("div");
    dateDiv.innerHTML = `<i>${convertDateFormat(element["fields"]["date_time"])}`;
    dateDiv.classList.add("ml-auto");
    postfixDiv.appendChild(dateDiv);
    
    const separator = document.createElement("hr");
    article.appendChild(separator);
    return article;
}
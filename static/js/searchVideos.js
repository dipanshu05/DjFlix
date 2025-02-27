const searchField = document.querySelector("#searchField");
const childDiv = document.querySelector(".mix");
const paginationContainer = document.querySelector(".pagination__option");
const noResults = document.querySelector(".no-results");
const parentDiv = document.querySelector("#all_videos");

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    parentDiv.innerHTML = "";
    fetch("search_videos", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        childDiv.style.display = "none";

        if (data.length === 0) {
          noResults.style.display = "block";
        } else {
          noResults.style.display = "none";
          data.forEach((item) => {
            parentDiv.innerHTML += `
                <div class="col-lg-4 col-md-6 col-sm-6 mix ${item.category}">
                    <div class="portfolio__item" >
                        <div class="portfolio__item__video set-bg" data-setbg="/static/img/portfolio/portfolio-1.jpg" style='background-image: url("/static/img/portfolio/portfolio-1.jpg");'>
                            <a href="videos/${item.slug}" class="play-btn video"><i
                                    class="fa fa-play"></i></a>
                        </div>
                        <div class="portfolio__item__text">
                            <h4>${item.name}</h4>
                        </div>
                    </div>
                </div>`;
          });
        }
      });
  } else {
    // function includeJs(jsFilePath) {
    //   var js = document.createElement("script");
  
    //   js.type = "text/javascript";
    //   js.src = jsFilePath;
  
    //   document.body.appendChild(js);
    // }
    // includeJs("/static/js/pagination.js");
    parentDiv.style.display = "block";
    paginationContainer.style.display = "block";
    noResults.style.display = "none";
  }
});
    const recordsDisplay = document.getElementById('all_videos');
    const total_records_div = recordsDisplay.querySelectorAll(':scope > .mix');
    const records_per_page = 6;
    let page_number = 1;
    const total_records = total_records_div.length;
    const total_page = Math.ceil(total_records / records_per_page);
    const filter = document.getElementById('row');
    const fil = document.querySelector('.fil');
    const liFilter = document.querySelector('.portfolio__filter');
    const totalLi = liFilter.querySelectorAll(':scope > .fil');
    const firstli = document.querySelector('.first');

    generatePage();
    DisplayRecords();
    function DisplayRecords(){
        let start_index = (page_number - 1) * records_per_page;
        let end_index = start_index + (records_per_page - 1);
        if(end_index >= total_records){
            end_index = total_records - 1;
        }
        let statement = '';

        fetch("pagination",{
            method: "GET",
        })
        .then((res) => res.json())
        .then((data) => {
            for(let i=start_index; i<=end_index; i++){
                statement += `<div class="col-lg-4 col-md-6 col-sm-6 mix ${data[i].category}"> ${total_records_div[i].innerHTML} </div>`;
                recordsDisplay.innerHTML = statement;
                document.querySelectorAll('.dynamic-item').forEach(item=>{
                    item.classList.remove('active-number');
                })
                document.getElementById(`page${page_number}`).classList.add('active-number');

                if(page_number == 1){
                    document.getElementById('prevBtn').classList.add('disabled');
                }else{
                    document.getElementById('prevBtn').classList.remove('disabled');
                }

                if(page_number == total_page){
                    document.getElementById('nextBtn').classList.add('disabled');
                }else{
                    document.getElementById('nextBtn').classList.remove('disabled');
                }
            }
        });
    }
    
    function generatePage(){
        
        let prevBtn = `<a href="javascript:void(0)" id="prevBtn" class="arrow__pagination left__arrow" 
                        onclick = "prevBtn()"><span class="arrow_left"></span> Prev</a>`;
        let nextBtn = `<a href="javascript:void(0)" id="nextBtn" class="arrow__pagination right__arrow" 
                        onclick = "nextBtn()">Next <span class="arrow_right"></span></a>`;
        let buttons = '';
        let activeClass = '';

        for(let i=1; i<= total_page; i++){
            if(i == 1){
                activeClass = 'active-number';
            }
            else{
                activeClass = '';
            }
            buttons += `<a href="javascript:void(0)" onclick="page(${i})" 
                        class="number__pagination dynamic-item ${activeClass}" id="page${i}">${i}</a>`;
        }

        document.getElementById('pagination').innerHTML = `${prevBtn}${buttons}${nextBtn}`;
    }

    function nextBtn(){
        totalLi.forEach((item) => {
            item.classList.remove("active");
        });
        firstli.classList.add("active");
        recordsDisplay.classList.remove("mixitup-container-failed");
        page_number++;
        DisplayRecords();
    }

    function prevBtn(){
        totalLi.forEach((item) => {
            item.classList.remove("active");
        });
        firstli.classList.add("active");
        recordsDisplay.classList.remove("mixitup-container-failed");
        page_number--;
        DisplayRecords();
    }
    
    function page(index){
        totalLi.forEach((item) => {
            item.classList.remove("active");
        });
        firstli.classList.add("active");
        recordsDisplay.classList.remove("mixitup-container-failed");
        page_number = parseInt(index);
        DisplayRecords();
    }
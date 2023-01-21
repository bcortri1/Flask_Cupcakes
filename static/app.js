const $list = $('#c-list');
const $btn = $('#c-btn');


function updateCupcakeList(cupcake , list){
    const $cupcake = $(`<li>${cupcake.size} ${cupcake.flavor}</li>`);
    list.append($cupcake);
}

async function populateList(){
    const response = await axios.get('/api/cupcakes');

    for (let cupcake of response.data.cupcakes){
        updateCupcakeList(cupcake, $list);
    }
}


$btn.on("click", async function(evt){
    evt.preventDefault();
    let cupcake = {}
    cupcake.size = $('#size').val();
    cupcake.flavor = $('#flavor').val();
    cupcake.rating = $('#rating').val();
    cupcake.image = $('#image').val();
    updateCupcakeList(cupcake, $list);
    let result = await axios.post('/api/cupcakes',{...cupcake})
    console.log(result)
})


populateList();
<template>
  <div class="pizza-card">
    <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M15 3C8.37258 3 3 8.37258 3 15C3 21.6274 8.37258 27 15 27C21.6274 27 27 21.6274 27 15C27 8.37258 21.6274 3 15 3ZM15 23.2505C14.1716 23.2505 13.5 22.579 13.5 21.7505V12.7985C13.5 11.97 14.1716 11.2985 15 11.2985C15.8284 11.2985 16.5 11.97 16.5 12.7985V21.7505C16.5 22.579 15.8284 23.2505 15 23.2505ZM13.5 8.24859C13.5 7.4207 14.1716 6.74957 15 6.74957C15.8284 6.74957 16.5 7.4207 16.5 8.24859C16.5 9.07647 15.8284 9.74761 15 9.74761C14.1716 9.74761 13.5 9.07647 13.5 8.24859Z" fill="#BF0200"/>
      <path fill-rule="evenodd" clip-rule="evenodd" d="M3 15C3 8.37258 8.37258 3 15 3C21.6274 3 27 8.37258 27 15C27 21.6274 21.6274 27 15 27C8.37258 27 3 21.6274 3 15ZM15 0C6.71573 0 0 6.71573 0 15C0 23.2843 6.71573 30 15 30C23.2843 30 30 23.2843 30 15C30 6.71573 23.2843 0 15 0Z" fill="#BF0200"/>
    </svg>
    <img src="../img/pizza.png" class="pizza_pic"/>
    <span class="card-title">пепперони</span>
    <span class="card-price">450 руб.</span>
    <div class="card-button">
      <span class="card-button__title">добавить</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VPizzaCard',
  // props: {
  //   msg: String
  // }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.pizza-card{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 390px;
  width: 250px;
  background-color: #FFEFD2;
  border: 3px solid #BF0200;
  border-radius: 30px;
  padding: 20px;
}
.pizza_pic{
  height: 235px;
  width: 224px;
}
.card-title{
  font-family: Nunito;
  font-size: 2.2rem;
  color: #CA151C;
}
.card-price{
  font-family: Nunito;
  font-size: 1.7rem;
  color: #CA151C;
  font-weight: 300;
}
.card-button{
  background-color: #BF0200;
  width: 100%;
  text-align: center;
  border-radius: 25px;
  padding: 8px 0px;
  margin-top: 15px;
}
.card-button__title{
  font-family: Nunito;
  font-size: 1.5rem;
  color: #FFF9ED;
  font-weight: 300;
}
svg{
  align-self: flex-end;
  /* margin: 0px 15px; */
  margin-bottom: -30px;
}
</style>

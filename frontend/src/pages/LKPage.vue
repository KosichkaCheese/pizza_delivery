<template>
    <div class="LK-page">
        <VHeader :title="'личный кабинет'"></VHeader>
        <!-- <VPizzaBasketCard></VPizzaBasketCard>
        <div class="card-button">
          <span class="card-button__title">очистить корзину</span>
        </div>
        <span class="basket-page__sum">итого: 700 руб.</span>
        <div class="card-button">
          <span class="card-button__title">оформить заказ</span>
        </div> -->
    </div>
</template>

<script>

// import ArrowLeftSVG from '@/img/arrowLeftSVG.vue';
import VHeader from '../components/VHeader.vue';
// import VPizzaBasketCard from '../components/VPizzaBasketCard.vue'

export default {
    name: 'LKPage',
    components: {
        // ArrowLeftSVG,
        VHeader,
        // VPizzaBasketCard,
    }
}
</script>

<style>
.LK-page__title{
    background-color: #FFE9C1;
    border: 4px solid #CA151C;
    border-radius: 50px;
    width: 95%;
    height: auto;
    color: #CA151C;
    margin: 30px 50px;
    text-align: center;
    font-family: Nunito;
    font-size: 2.7rem;
    font-weight: 800;
    justify-self: center;
}

</style>

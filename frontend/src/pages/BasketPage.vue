<template>
    <div class="basket-page">
        <VHeader :title="'корзина'"></VHeader>
        <VPizzaBasketCard></VPizzaBasketCard>
        <div class="basket-page__actions">
            <VButtonWhite :title="'очистить корзину'"></VButtonWhite>
            <span class="basket-page__sum">итого: 700 руб.</span>
        </div>
        <VButtonRed :title="'оформить заказ'"></VButtonRed>
        <!-- <div class="card-button">
            <span class="card-button__title">оформить заказ</span>
        </div> -->
    </div>
</template>

<script>

// import ArrowLeftSVG from '@/img/arrowLeftSVG.vue';
import VPizzaBasketCard from '../components/VPizzaBasketCard.vue'
import VHeader from '../components/VHeader.vue';
import VButtonWhite from '../components/VButtonWhite.vue';
import VButtonRed from '../components/VButtonRed.vue';

export default {
    name: 'BasketPage',
    components: {
    // ArrowLeftSVG,
        VPizzaBasketCard,
        VHeader,
        VButtonWhite,
        VButtonRed,
    }
}
</script>

<style>
.basket-page{
    font-family: Nunito;
    color: #CA151C;
}
.basket-page__actions{
    display: flex;
    justify-content: space-between;
    margin: 0 90px;
}
.basket-page__sum{
    font-size: 1.8rem;
    font-weight: 800;
}
</style>

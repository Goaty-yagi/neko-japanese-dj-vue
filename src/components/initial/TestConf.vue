<template>
  <div class="test-conf">
    <article class='conf-wrapper'>
        <div class="conf-header ">
            <p class='has-text-white is-size-3'>実力テスト</p>
            <label class="checkbox">
                <input @click='getClass' type="checkbox" id='checkbox' v-model="checked">
                <i class='has-text-white is-size-6'>・以下の問題を複製しません。</i>
            </label>
        </div>
        <div class="conf-body">
            <router-link @click='closeConf' to=/ class="button d m-2">DISAGREE</router-link>
            <button 
              @click='getURL'
              class="button m-2 is-disabled"
              ref='buttonHover'
              :disabled='!checked'>AGREE</button>
        </div>
    </article>                     
  </div>
</template>

<script scoped>
export default {
    data(){
        return{
            checked: false
        }
    },
    mounted(){
        this.scrollTop()
    },
    methods:{
        closeConf(){
            this.$emit('close')
            this.$store.commit('reset')
        },
        getURL(){
            this.$router.push('/quiz-test-init')
            this.$store.commit('noticeOff')     
        },
        getClass(){
            if (this.checked == false){
                this.$refs.buttonHover.classList.add('button-hover')
            }else{
                this.$refs.buttonHover.classList.remove('button-hover')
            }   
        },
        resultHandler(){
            this.$store.commit('testHandler')
        },
        scrollTop(){
            window.scrollTo({
            top: 0,
            });
        },
    }
}
</script>

<style lang='scss' scoped>
@import "style/_variables.scss";
    .test-conf{
        display: flex;
        align-items: center;
        height: 100vh;
        }.conf-wrapper{
            border-radius: 1rem;
            overflow:hidden;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 10rem;
            }
    .button{
    border-radius: 100vh;
    border: 2px solid $base-color;
    margin:1rem;
    padding:0.4rem;
    background: transparent;
    color: $base-color;
    font-weight:bold;
    font-size: 1rem;
    transition:0.5s;
    &.d:hover{
        color:green;
        }
    &.button-hover{
        background: $base-color;
        color:white;
    }
    }
    .conf-body{
        padding:2rem;
    }
</style>
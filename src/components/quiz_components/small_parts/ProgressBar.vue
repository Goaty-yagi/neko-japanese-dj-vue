<template>
  <div class="progress-wrapper">
    <div v-if="!showProgressBar" class="progress-bar-outer">
        <div id="progress" class="progress-bar-inner"></div>
    </div>
</div>
</template>

<script>
// progressConfig looks loke this
// progressConfig:{
// }
export default {
    props: [
        'divisor',
        'numToBeDevided',
        'showProgressBar',
        'progressConfig'
    ],
    data(){
        return {

        }
    },
    mounted() {
      console.log('PROGRESS_MOUNTED',this.divisor,this.numToBeDevided)
        const progressElement = document.getElementById('progress')
        progressElement.setAttribute('style',`width:0%`)
    },
    beforeUnmount() {

    },
    computed:{
        result() {
            return showProgressBar
        }
    },
    methods:{
        progressBar(){
            const percentage = this.divisor/(this.numToBeDevided) * 100 
            const progressElement = document.getElementById('progress')
            progressElement.setAttribute('style',`width:${percentage}%`)
        },
        setToZero() {
          const progressElement = document.getElementById('progress')
          progressElement.setAttribute('style',`width:0%`)
        }
    }

}
</script>

<style scoped lang="scss">
@import "style/_variables.scss";

.progress-wrapper {
  display: flex;
  justify-content: center;
  min-height: 80%;
  .progress-bar-outer {
    position: relative;
    border: solid black;
    border-radius: 50vh;
    width: 80%;
    height: 2rem;
    background: rgb(238, 238, 238);
    margin-bottom: 1.5rem;
    margin-top: 0.5rem;
    overflow: hidden;
    .progress-bar-inner {
      position: absolute;
      top: 0;
      left: 0;
      box-sizing: inherit;
      height: 1.8rem;
      transform: skewX(-10deg);
      transition: 1s;
      background: linear-gradient(to bottom right, #f6f3e4 1%, #ffc890);
    }
  }
}
@media (max-width: 480px) {
  .progress-bar-outer {
    margin-bottom: 0.5rem !important;
    margin-top: 0 !important;
  }
}
</style>
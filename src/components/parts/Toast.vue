<template>
  <div class="toast__wrapper" ref="mostOutWrapper">
      <div class="toast-notification">
        <div class="toast-notification-text">
            <p>{{toastConfig.mainText}}</p>
            <p>{{toastConfig.subText}}</p>
        </div>
    </div>
</div>
</template>

<script>
// parent of this toast component should be relative potision
// toastConfig looks like this 
// toastConfig:{
//     mainText:'are you sure?',
//     confirmFun: this.patchQuestionSolved,
//     confirmText:'Sure'
// }

const globalInstanceList = [];

import Animation from "@/components/parts/Animation.vue";
export default {
  components: {
    Animation,
    },
    props: [
      "toastConfig",
    ],
    data() {
      return {
        showPopover: false,
        instanceId: 0,
        parentElement: {},
        reloadDetector:''
      }
    },
    created() {
    },
    mounted(){
        console.log("MOUN")
    },
    watch: {
  },
    computed:{
    },
    methods:{
      
    }
}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";
/* Popover styling */
.toast__wrapper{
    position: absolute;
    width: 100%;
    bottom: 0;
    height: 10px;
    .toast-notification {
        border:0.2rem solid $dark-blue;
        color: blue;
        background: rgb(197, 240, 250);
    }
}



</style>
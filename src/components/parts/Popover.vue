<template>
  <div class="popover__wrapper" ref="mostOutWrapper">
    <Animation ref="animation">
      <div class="popover__content" ref="contentRef">
        <div class="close-icon">
            <i class="fas fa-times"></i>
        </div>
          <p class="popover__message">{{ popoverConfig.mainText }}</p>
          <div class="buttons">
            <i v-if="smallIsLoading" class="fas fa-spinner fa-pulse"></i>
            <div v-if="!smallIsLoading">
              <button @click="confirm" class="btn-litegray-black-gray-sq">{{ popoverConfig.confirmText }}</button>
            </div>
        </div>
      </div>
    </Animation>
</div>
</template>

<script>
// parent of this popover component should be relative potision
// popoverConfig looks like this 
// popoverConfig:{
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
      "popoverConfig",
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
      console.log('created', this.$route)
      this.reloadDetector = this.$route.name
    },
    mounted(){
      this.initialization()
      this.initialNodeConfig()
        console.log("POPOVER",window.innerWidth)
    },
    watch: {
    $route(to) {
      if(typeof this.reloadDetector !== 'undefined') {
        this.parentElement.removeEventListener('click', (e) => {
          if(!this.functionEnabled()) {
            e.stopPropagation()
            this.showPopoverHandler()
          }
        })
        this.animationOut()
        globalInstanceList.length = 0
        this.initialization()
        this.initialNodeConfig()
        } else [
          this.reloadDetector = this.$route.name
        ]
      console.log("route-change", this.$route, this.reloadDetector)
    }
  },
    computed:{
        smallIsLoading() {
            return this.$store.getters.smallIsLoading
        }
    },
    methods:{
      globalInstanceFunction() {
        if (this.showPopover) {
          this.showPopover = !this.showPopover;
        }
      },

      initialization() {
        const obj = {
          open: false,
          function: this.globalInstanceFunction,
        };
        globalInstanceList.push(obj);
        this.instanceId = globalInstanceList.length - 1;
      },
      initialNodeConfig() {
        console.log("initial_config")
        this.parentElement = this.$refs.mostOutWrapper.parentElement;
        const mostOutWrapper = this.$refs.mostOutWrapper
        const parentHeight = this.parentElement.offsetHeight
        mostOutWrapper.style.top = parentHeight + 'px'

        console.log(this.parentElement)
        this.parentElement.addEventListener('click', (e) => {
          if(!this.functionEnabled()) {
            e.stopPropagation()
            this.showPopoverHandler()
          }
        })

        const windowWidth = window.innerWidth
        const contentRefCoordinate = this.$refs.contentRef.getBoundingClientRect()
        const leftSum = contentRefCoordinate.left + contentRefCoordinate.width
        const Difference = leftSum - windowWidth

        if(Difference > 0) {
          const parentElementCoordinate = this.parentElement. getBoundingClientRect()
          const containerDiffer =  contentRefCoordinate.width - parentElementCoordinate.width
          if(containerDiffer > 0) {
            mostOutWrapper.style.right = containerDiffer / 2 + 'px'
          }
        }
        console.dir(this.$refs.contentRef)
        console.log(this.$refs.contentRef.getBoundingClientRect())
      },
      showPopoverHandler() {
        console.log("clicked", globalInstanceList.length )
        this.$refs.animation.animationHandler();
        this.showPopover = !this.showPopover;
        if(globalInstanceList.length > 1) {
          globalInstanceList[this.instanceId].open = true
          for(let i = 0; i < globalInstanceList.length; i ++) {
            console.log(i, this.instanceId)
            if(i !== this.instanceId)
            globalInstanceList[i].function()
          }
        }
      },
      animationOut() {
        this.$refs.animation.animationOut();
      },
      async confirm() {
          await this.popoverConfig.confirmFun()
          
      },
      functionEnabled() {
        return !this.$refs.animation.animationEnd;
      },
    }
}
</script>

<style lang="scss" scoped>
@import "style/_variables.scss";
/* Popover styling */

a {
  text-decoration: none;
}

.popover__wrapper {
  width: 100%;
  position: absolute;
  display: flex;
  justify-content: center;
  z-index: 1;
}
.popover__content {
  /* opacity: 0; */
  /* visibility: hidden; */
  position: flex;
  justify-content: center;
  border-radius: 0.2rem;
  transform: translate(0, 10px);
  background-color: #313131;
  padding: 0.5rem;
  min-width: 180px;
  box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.26);
  border: solid gray;
  /* box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px; */
  min-width: 180px;
}
.popover__content:before {
  position: absolute;
  z-index: -1;
  content: "";
  right: calc(50% - 10px);
  top: -8px;
  border-style: solid;
  border-width: 0 10px 10px 10px;
  border-color: transparent transparent #313131 transparent;
  transition-duration: 0.3s;
  transition-property: transform;
}
/* .popover__wrapper:hover .popover__content {
  z-index: 10;
  opacity: 1;
  visibility: visible;
  transform: translate(0, -20px);
  transition: all 0.5s cubic-bezier(0.75, -0.02, 0.2, 0.97);
} */
.popover__message {
  text-align: center;
  color: rgb(251, 251, 251);
}
.buttons {
    margin-top: 0.2rem;
    display: flex;
    justify-content: center;
}
.btn-litegray-black-gray-sq {
    margin: 0.3rem;
    min-width: 50px;
    padding: 0 0.2rem;
    font-size: 0.7rem;
}

  .close-icon {
    font-size: 0.7rem;
    position: absolute;
    top: 0;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    border: solid rgb(180, 179, 179);
    border-radius: 50vh;
    width: 1rem;
    height: 1rem;
    margin-top: 0.1rem;
    margin-right: 0.1rem;
    color: rgb(172, 172, 172);
    transition: 0.3s;
    z-index: 2;
  }
  .close-icon:hover {
    border: solid rgb(216, 215, 215);
    color: rgb(216, 215, 215);
  }


</style>
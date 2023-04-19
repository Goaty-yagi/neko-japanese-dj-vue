<template>
  <div ref="parentRef" :style="{'z-index':animationStarted?'1':'-100'}" class='parent'>
    <div :style="{visibility:animationStarted?'':'hidden','z-index':animationStarted?'0':'-100'}" :class="animationStarted?'in-animation':''" ref="slot">
      <slot slot="animation"></slot>
    </div>
  </div>
</template>

<script>
const globalInstanceList = [];

export default {
  // props: [
  //   "animationConfig",
  // ],
  data() {
    return {
      animationStarted: false,
      animationEnd:true,
      animationEndUnenabled: false
    };
  },
  created() {
    // const obj = {
    //   function: this.globalInstanceFunction,
    // };
    // globalInstanceList.push(obj);
    // this.instanceId = globalInstanceList.length;
  },
  mounted() {
    this.initialization()
    console.log('mounted',this.animationStarted, this.instanceId)
  },
  beforeUnmount() {
    console.log("animation_B_UNMOUNT")
    this.beforeUnmountEvent()
  },
  watch: {
    $route(to) {
      // globalInstanceList.length = 0
    }
  },
  computed: {
    firstChildElement() {
      return this.$refs.slot;
    },
  },
  methods: {
    initialization() {
      const obj = {
        function: this.globalInstanceFunction,
      };
      obj['parentRef'] = this.$refs.parentRef
      obj['slotRef'] = this.$refs.slot
      obj['aminationOn'] = false
      obj['open'] = false
      obj['instance'] = this
      globalInstanceList.push(obj);
      this.instanceId = globalInstanceList.length -1 ;
      console.log('anime_initial',obj['instance'])
    },
    globalInstanceFunction() {
      console.log("list", globalInstanceList, this.instanceId,  globalInstanceList[this.instanceId].open)
      if(globalInstanceList[this.instanceId].open) {
        console.log("open-desu")
        const parentRef = globalInstanceList[this.instanceId].parentRef
        const slotRef = globalInstanceList[this.instanceId].slotRef

        parentRef.classList.remove("in-animation")
        const copiedElement = slotRef.cloneNode("deep");
        copiedElement.classList.add("out-animation")

        parentRef.removeChild(slotRef);
        parentRef.appendChild(copiedElement);
        globalInstanceList[this.instanceId].open = false
        copiedElement.addEventListener("animationend", () => {
          slotRef.classList.add("in-animation")
          parentRef.appendChild(slotRef)
          parentRef.removeChild(copiedElement);
          copiedElement.removeEventListener("animationend", this.animatedEvent)
          this.animationStarted = !this.animationStarted;
          this.animationEnd = true
        })
      }

    },
    animationHandler() {
      console.log("HANDLER",globalInstanceList, this.instanceId)
      if(globalInstanceList.length > 1) {
        for(let i = 0; i < globalInstanceList.length; i ++) {
          if(i !== this.instanceId)
          globalInstanceList[i].function()
        }
      }
      this.animationEnd = false
      if(this.animationStarted&&!this.animationEndUnenabled){
        const parentRef = this.$refs.parentRef
        const slotRef = this.$refs.slot

        slotRef.classList.remove("in-animation")
        const copiedElement = slotRef.cloneNode("deep");
        copiedElement.classList.add("out-animation")

        parentRef.removeChild(slotRef);
        parentRef.appendChild(copiedElement);

        copiedElement.addEventListener("animationend", () => this.animatedEvent(slotRef,parentRef,copiedElement))
      } else {
        this.animationStarted = !this.animationStarted;
        globalInstanceList[this.instanceId].open = true
        const slotRef = this.$refs.slot
        slotRef.addEventListener("animationend",() => {console.log("END"), this.animationEnd = true})
      }
    },
    animatedEvent(slotRef, parentRef, copiedElement) {
        slotRef.classList.add("in-animation")
        parentRef.appendChild(slotRef)
        parentRef.removeChild(copiedElement);
        copiedElement.removeEventListener("animationend", this.animatedEvent)
        this.animationStarted = !this.animationStarted;
        this.animationEnd = true
        globalInstanceList[this.instanceId].open = false

    },
    animationOut() {
      if(this.animationStarted){
        const parentRef = this.$refs.parentRef
        const slotRef = this.$refs.slot

        slotRef.classList.remove("in-animation")
        const copiedElement = slotRef.cloneNode("deep");
        copiedElement.classList.add("out-animation")

        parentRef.removeChild(slotRef);
        parentRef.appendChild(copiedElement);

        copiedElement.addEventListener("animationend", () => this.animatedEvent(slotRef,parentRef,copiedElement))
      }
    },
    beforeUnmountEvent(instanceId) {
      globalInstanceList.splice(instanceId, 1)
      if(globalInstanceList.length)
      console.log('len',globalInstanceList.length)
      for (let i = 0; i < globalInstanceList.length; i ++) {
        globalInstanceList[i].instance.instanceId = i
      }
      this.animationEndUnenabled = false
      console.log("BU_END", globalInstanceList)
    },
    animationEndUnenabledHandler() {
      console.log('ANIMEHANDLE',this.animationEndUnenabled)
      this.animationEndUnenabled = true
    }
  },
};
</script>

<style scoped lang="scss">
@import "style/_variables.scss";
.parent {
  width: 100%;
  height: 0px;
  top: 0;
  position: absolute;
  display: inline-block;
  z-index: 1;
}
.in-animation {
  width: 100%;
  display: flex;
  justify-content: center;
  position: absolute;
  animation: bottomToUp 0.5s ease-out forwards;
}
.out-animation {
  width: 100%;
  display: flex;
  justify-content: center;
  position: absolute;
  animation: bottomToUp 0.5s ease-out reverse forwards;
}

@keyframes bottomToUp {
  0% {
    opacity: 0;
    top: 35px;
  }
  100% {
    opacity: 1;
    top: 0px;
  }
}
</style>
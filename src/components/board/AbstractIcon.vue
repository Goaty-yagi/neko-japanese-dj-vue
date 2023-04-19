<template>
  <div @click="clickEvent" class="ab-icon-wrapper" ref='mostOuterRef'>
    <div v-show="!clicked" class="no-favorite">
        <i ref='unclickedRef' :class="[clicked? 'display-none':config.icons.unclicked.icon ]"> </i>
    </div>
    <div class="clicked-icon" ref='parentRef'>
        <div ref='animationRef'>
            <i ref='clickedBorderRef' v-if="iconAsBorderCheck" :class="config.icons.unclicked.icon"></i>
            <i ref='clickedRef' :class="config.icons.clicked.icon"></i>
        </div>
    </div>
  </div>
</template>

<script>
export default {
//config looks like this
//config: {
//     clickEvent: this.handleAddedFavorite, // necessary
// clickEventEnabled: if false, click will be unenabled. default is true
//     unclickEvent:'' if click and unclick are differ event
//     enableUnclickEvent: true,default is true,  
//     clickEvent: this.handleAddedFavorite,
        // icons:{
        //     clicked:{
        //         icon:'fas fa-star',
        //         color:'yellow'
        //     },
        //     unclicked:{
        //         icon:'far fa-star',
        //         color:'',
        //         borderColor:''
        //     },
        //     asBorder:true
        // }
// }
// eventArguments looks like this 
// {
//     clickEvent: answerId
// }
props:[
    'config',
    'clicked',
    'eventArguments'
],
  data() {
    return {
      iconClassName:'',
      copiedAnimationElement:{},
      parentRef: {},
      animationRef: {},
      initialized: false
    };
  },
  beforeMount() {
  },
  mounted() {
    this.initialization()
  },
  computed: {
    enableUnclickedEvent() {
        if(typeof this.config.enableUnclickEvent !== 'undefined') {
            return this.config.enableUnclickEvent
        } else {
            return true
        }
    },
    eventClickArgumentCheck() {
      if(typeof this.eventArguments !== 'undefined') {
        try{
          return this.eventArguments.clickEvent
        } catch {
          //not yet tested
          Error("eventArgument dosn't include clickEvent")
        }
      }
    },
    uneventClickArgumentCheck() {
      if(typeof this.eventArguments.unclickEvent !== 'undefined') {
        try{
          return this.eventArguments.unclickEvent
        } catch {
          //not yet tested
          Error("eventArgument dosn't include unclickEvent")
        }
      }
    },
    unclickEventExist() {
      if(typeof this.config.unclickEvent !== 'undefined') {
        return this.config.unclickEvent
      } else {
        return false // default is false means click and unclick are the same eve or np unclick eve
      }
    },
    iconAsBorderCheck() {
      if(typeof this.config.icons.asBorder !== 'undefined') {
            return this.config.icons.asBorder
        } else { 
            return true // default is true
        }
    }
    
  },
  methods: {
    initialization() {
        this.colorSetting()
        console.log("checkCLICKED",this.clicked)
         //need to think about if the icon is not 1rem
        const parentOfThisRef = this.$refs.mostOuterRef.parentElement
        const outerWrapperRef = this.$refs.mostOuterRef
        const parentHeight = parentOfThisRef.offsetHeight
        outerWrapperRef.style.height = parentHeight + 'px'

        this.parentRef = this.$refs.parentRef
        this.animationRef = this.$refs.animationRef
        this.copiedAnimationElement = this.$refs.animationRef.cloneNode("deep");
        this.copiedAnimationElement.className = 'animation'
        if(!this.clicked) {
          console.log("DELETE")
            this.parentRef.removeChild(this.animationRef)
        }
    },
    colorSetting() {
        const unclickedRef = this.$refs.unclickedRef
        const clickedRef = this.$refs.clickedRef
        const clickedBorderRef = this.$refs.clickedBorderRef
        if(typeof this.config.icons.clicked.color !== 'undefined') {
            clickedRef.style.color = this.config.icons.clicked.color
        }
        if(typeof this.config.icons.unclicked.color !== 'undefined') {
            unclickedRef.style.color = this.config.icons.unclicked.color
        }
        if(typeof this.config.icons.unclicked.borderColor !== 'undefined') {
            clickedBorderRef.style.color = this.config.icons.unclicked.borderColor
        }
    },
    async clickEvent() {
        if(!this.undefinedChekerTrue(this.config,'clickEventEnabled')) {
          await this.config.clickEvent(this.eventClickArgumentCheck)
          return
        }
            if(!this.clicked) {
                this.initialized = true
                this.parentRef.appendChild(this.copiedAnimationElement)
            } else if (!this.enableUnclickedEvent) { 
                return             
            } else if (this.parentRef.contains(this.animationRef)) {
                this.parentRef.removeChild(this.animationRef)
            } else {
                this.parentRef.removeChild(this.copiedAnimationElement)
            }


            if(this.unclickEventExist) {
                   await this.config.unclickEvent(this.uneventClickArgumentCheck) // not yet tested
            } else {
                await this.config.clickEvent(this.eventClickArgumentCheck)
            }
            console.log("done",this.clicked, this.initialized)
    },
    undefinedChekerTrue(obj, arg) {
        //check obj.somethig exist. true will be returned as default
        console.log('OBJ',obj[arg])
        if(typeof obj[arg] !== 'undefined') {
            return obj[arg]
        } else {
            return true
        }
    }
  },
};
</script>

<style scoped lang='scss'>
.ab-icon-wrapper {
  position: relative;
  .no-favorite {
    position: relative;
    width: 1rem;
    height: 1rem;
    .far {
        top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      position: absolute;
    }
    .display-none {
      display: none;
    }
  }
  .clicked-icon {
    width: 1rem;
    height: 1rem;
    .animation {
        width: 100%;
        height: 100%;
        position: absolute;
        animation: icon 0.5s ease-out forwards;
    }
    .far {
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      position: absolute;
      z-index: 2;
    }
    .fas {
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      position: absolute;
      z-index: 1;
    }
  }
}
@keyframes icon {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}
</style>
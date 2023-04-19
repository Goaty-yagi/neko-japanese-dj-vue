<template>
  <div
    class="form-select-container"
    :style="{ height: parentHeight + 'px' }"
    ref="mostOutWrapper"
  >
    <div
      class="enquire-type"
      @click="!chosenItem && !functionEnabled ? showOptions() : ''"
      ref="animationWrapper"
    >
      <i
        v-if="!chosenItem && caluculatedShowArrow()"
        class="fas fa-angle-down"
        :class="{ lotate: showOptionList }"
        ref="arrowRef"
      >
      </i>
      <div
        v-if="chosenItem && caluculatedShowChosenItem"
        :style="chosenTextStyle"
      >
        {{ chosenItem }}
      </div> 
      <Animation ref="animation">
        <div class="type-select" ref="selectContainer">
          <div
            class="select-loop"
            @click="showOptions()"
            v-for="(option, index) in choicesArray"
            v-bind:key="index"
          >
            <div @click.stop="getSelectedOption(option)">
               <p
              class="type"
              ref="optionContainer"
            >
              <span v-if="!caluculatedIsFont">
                <span v-if="caluculatedBullet === 'same'">{{
                  bulletObj.bullet
                }}</span>
                <span v-if="caluculatedBullet === 'num'"
                  >{{ index + 1 }} {{ bulletObj.bullet }}</span
                >
                <span v-if="caluculatedBullet === 'array'">{{
                  arrayBullets(index)
                }}</span>
              </span>
              <span v-if="caluculatedIsFont">
                <span v-if="caluculatedBullet === 'array'">
                  <i :class="arrayBullets(index)"></i>
                </span>
                <span v-if="caluculatedBullet === 'same'">
                  <i :class="bulletObj.font"></i>
                  {{ bulletObj.bullet }}
                </span>
              </span>
              {{ option }}
            </p>
              
            </div>
          </div>
        </div>
      </Animation>
      <i
        @click="chosenItem && !functionEnabled ? showOptions() : ''"
        v-if="chosenItem && caluculatedShowChosenItem"
        class="fas fa-edit"
      ></i>
    </div>
  </div>
</template>

<script>
// ** necessary actions

// parent should be one,
// parent needs to set getSelectedItem function like below
// clickTypeConfig.function must be set. this will fire when a option is clicked

// choicesArray necessary: must be Array

// **not necessary action

// chosenTextStyle (must be obj) not necessary: can include fontsize, fontwight, color like below
// {fontSize: '1.2rem', fontWeight: 'bold', color: 'pink'}

//clickTypeConfig: not necessary:
// clickTypeConfig: {
//     showArrow: true, default is true
//     arrowPlace:'right', default is center
//     arrowColor:'white', default is black
//     function: this.goStart,
//     clickMovePage:true, this is for moveout animation will be none is true, default is false
//     showChosenItem: false, defult is true 
//  },

// optionAlign not necessary: default is center

// bulletObj not necessary: can include type, bullet, array(must be array)
// this is for specific bullets. if none, will be defaul which is no bullet.
// example
// bulletObj:{
//   type:'array' => not necessary, here must be 'array', 'num' or 'same' if need.
//   bullet:',' => bullet string which will be set before each option.
//   array:['z','z','a','d','r','r','q'] => length must be the same as choicesArray.length.
// }

// hoverObj include css style for parent which will be mouseover event

import Animation from "@/components/parts/Animation.vue";

const globalshowOptionList = [];

export default {
  components: {
    Animation,
  },
  props: [
    "choicesArray",
    "chosenTextStyle",
    "clickTypeConfig",
    "optionAlign",
    "bulletObj", // can be array, num, or specific type of bullet
    "hoverObj",
  ],
  data() {
    return {
      // functionEnabled: false,
      instanceId: 0,
      chosenItem: "",
      showOptionList: false,
      click: false,
      spin: false,
      parentHeight: "",
      parentPaddingTop: "",
      originalStyle: {},
      animationConfig:{

      }
    };
  },
  created() {
    const obj = {
      open: false,
      function: this.globalInstanceFunction,
    };
    globalshowOptionList.push(obj);
    this.instanceId = globalshowOptionList.length -1;
    console.log(this.instanceId);
    console.log("created", globalshowOptionList);
  },
  // beforeMount() {
  // },
  mounted() {
    this.getParentStyleInfo();
    this.mouseOverEvent();
  },
  beforeUnmount() {
    globalshowOptionList.length = 0;
  },
  computed: {
    caluculatedIsFont() {
      // for bulletObj
      if (typeof this.bulletObj !== "undefined") {
        if ("isFont" in this.bulletObj) {
          return this.bulletObj.isFont ? true : false;
        } else {
          return false;
        }
      } else {
        return false;
      }
    },
    caluculatedBullet() {
      // for bulletObj
      if (typeof this.bulletObj !== "undefined") {
        try {
          if ("type" in this.bulletObj) {
            // so the type not necessary here
            switch (this.bulletObj.type) {
              case "array":
                return "array";
                break;
              case "num":
                return "num";
                break;
              case "same":
                return "same";
                break;
            }
          } else {
            return false;
          }
        } catch (e) {
          if (e instanceof TypeError) {
            throw "TypeError, your bulletObj might be empty. it should be object or {}";
          } else {
            throw "error at bulletObj";
          }
        }
      }
    },
    caluculatedShowChosenItem() {
      if (typeof this.clickTypeConfig !== "undefined") {
        if ("showChosenItem" in this.clickTypeConfig) {
          return this.clickTypeConfig.showChosenItem;
        } else {
          return true;
        }
      } else {
        return true;
      }
    },
    getGlobalshowOptionList() {
      return globalshowOptionList;
    },
    functionEnabled() {
      return !this.$refs.animation.animationEnd;
    },
  },
  watch: {
  },
  methods: {
    getParentStyleInfo() {
      const parentElement = this.$refs.mostOutWrapper.parentElement;
      const computedStyle = getComputedStyle(parentElement);
      const borderTopWidth = parseFloat(computedStyle.borderTopWidth);
      const borderBottomWidth = parseFloat(computedStyle.borderBottomWidth);
      this.parentHeight =
        parentElement.offsetHeight - (borderTopWidth + borderBottomWidth);
    },
    globalInstanceFunction() {
      if (this.showOptionList) {
        this.showOptionList = !this.showOptionList;
      }
    },
    showOptions() {
      if(this.$refs.arrowRef) {
        if(!this.$refs.arrowRef.style.transition) {
          this.$refs.arrowRef.style.transition = '.3s'
        }
      }
      this.$refs.animation.animationHandler();
      this.showOptionList = !this.showOptionList;
      if(globalshowOptionList.length > 1) {
        console.log("more than one",  globalshowOptionList, this.instanceId)
        globalshowOptionList[this.instanceId].open = true
        for(let i = 0; i < globalshowOptionList.length; i ++) {
          console.log(i, this.instanceId)
          if(i !== this.instanceId)
          globalshowOptionList[i].function()
        }
      }

      const selectContainerRefs = this.$refs.selectContainer;
      if (this.showOptionList) {
        selectContainerRefs.style.top = this.parentHeight + 2 + "px";
        this.optionAlignHandler(selectContainerRefs);
      } 
    },
    showTypeHandle() {
      // how to think of implementing to animate when a node is disappeared
      // 1, prepare three css variable, first is static, second is in-animation, the last is out-animation.
      // 2, set ref to a node which you want to animate and the parent node of the node.
      // 3, create boolean variable in data, which handles status of animations. (in this case is animationOut)
      // 4, when out-animation trigger, get the parent and the node you want to animate(we call C-node),
      // remove in-animation class from C-node.

      this.spin = !this.spin;
      this.functionEnabled = true;

      if (this.animationOut) {
        const selectContainerRefs = this.$refs.selectContainer;
        selectContainerRefs.classList.remove("select-undisplay");
        selectContainerRefs.classList.add("type-select");
        selectContainerRefs.addEventListener("animationend", () => {
          this.animationOut = false;
          this.functionEnabled = false;
        });
      } else if (!this.animationOut) {
        // out-animation
        const animeRefs = this.$refs.animationWrapper;
        const selectContainerRefs = this.$refs.selectContainer;
        selectContainerRefs.classList.remove("type-select");
        this.copyNode = selectContainerRefs.cloneNode("deep");
        this.copyNode.classList.add("selectClose");
        animeRefs.removeChild(selectContainerRefs);
        animeRefs.appendChild(this.copyNode);
        this.copyNode.addEventListener("animationend", () => {
          this.animationOut = true;
          this.functionEnabled = false;
          animeRefs.removeChild(this.copyNode);
          selectContainerRefs.classList.add("select-undisplay");
          animeRefs.appendChild(selectContainerRefs);
        });
      }
    },
    getSelectedOption(option) {
      console.log("from_FORM_SELECT", this.undefinedChekerFalse(this.clickTypeConfig,'clickMovePage'))
      if(!this.undefinedChekerFalse(this.clickTypeConfig,'clickMovePage')) {
        this.showOptions();
        this.chosenItem = option;
        this.clickTypeConfig.function(option);
        console.log("GOTxx", this.chosenItem)
      } else {
        this.clickTypeConfig.function(option)
      }
    },
    arrayBullets(index) {
      if (this.caluculatedBullet !== "array") {
        return false;
      } else {
        if (!Array.isArray(this.bulletObj.array)) {
          throw new Error("bulletObj.array is not array!");
        } else {
          if (this.bulletObj.array.length !== this.choicesArray.length) {
            throw new Error(
              "bulletObj.array and choicesArray.length must be the same length!"
            );
          } else {
            return this.bulletObj.array[index];
          }
        }
      }
    },
    optionAlignHandler(selectContainerEelement) {
      // right, left, center(default), center-on-right, center-on-left
      // will be added some more for future update
      if (this.optionAlign === ("right" || "left" || "center")) {
        selectContainerEelement.style.textAlign = this.optionAlign;
      } else if (this.optionAlign === "center-on-left") {
        const optionElement = this.$refs.optionContainer;
        const baseWidth = optionElement.reduce((a, b, index) => {
          if ((a & b) !== "undefined") {
            return a.offsetWidth > b.offsetWidth ? a : b;
          } else {
            return a ? a : b;
          }
        }).offsetWidth;
        const fixedBaseWidth = baseWidth===0?fixedBaseWidth:baseWidth //assamption baseWidth is not 0 in the first place.
        for (let i = 0; i < optionElement.length; i++) {
          optionElement[i].style.width = fixedBaseWidth + 2 + "px";
          optionElement[i].style.textAlign = "left";
        }
      }
    },
    caluculatedShowArrow() {
      if (typeof this.clickTypeConfig !== "undefined") {
        if(typeof this.$refs.arrowRef!== "undefined") {
          if(this.$refs.arrowRef) {
             const arrowRef = this.$refs.arrowRef
            arrowRef.style[this.clickTypeConfig.arrowPlace] = 0
            arrowRef.style.color = this.clickTypeConfig.arrowColor
          }
        }

        if ("showArrow" in this.clickTypeConfig) {
          return this.clickTypeConfig.showArrow;
        } else {
          return true;
        }
      } else {
        return true;
      }
    },
    mouseOverEvent() {
      if (this.hoverObj) {
        const parentElement = this.$refs.mostOutWrapper.parentElement;
        parentElement.addEventListener("mouseenter", () => {
          for (let i in this.hoverObj) {
            this.originalStyle[i] = parentElement.style[i];
            parentElement.style[i] = this.hoverObj[i];
          }
          if (!parentElement.style.transition) {
            parentElement.style.transition = ".3s";
          }
        });
        parentElement.addEventListener("mouseleave", () => {
          for (let i in this.originalStyle) {
            parentElement.style[i] = this.originalStyle[i];
          }
        });
      }
    },
    undefinedChekerFalse(obj, arg) {
        //check obj.somethig exist. true will be returned as default
        console.log('OBJ',obj[arg])
        if(typeof obj[arg] !== 'undefined') {
            return obj[arg]
        } else {
            return false
        }
    },
    clearChosenItem() {
      this.chosenItem = ''
      console.log("clear", this.chosenItem)
    }
  },
};
</script>

<style scoped lang="scss">
@import "style/_variables.scss";
.form-select-container {
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  justify-content: center;
  width: 100%;
}
.enquire-type {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  // z-index: 1;
  .type-select {
    position: absolute;
    width: 100%;
    top: 0;
    background: rgba(37, 38, 62, 0.95);
    border-radius: 8px;
    border: solid $dark-blue;
    color: white;
    overflow: hidden;
    z-index: 1;
    .select-loop {
      transition: 0.3s;
    }
    .select-loop:hover {
      background: rgba(59, 60, 96, 0.75);
    }
  }
}
.select-undisplay {
  display: none;
}
.fa-angle-down {
  position: absolute;
  margin: 0 1rem;
  // transition: 0.5s;
}
.lotate {
  transform: rotate(180deg);
}
.type {
  padding: 0.5rem;
  display: inline-block;
}
.fa-edit {
  position: absolute;
  right: 1rem;
  transition: 0.3s;
}
.fa-edit:hover {
  color: gray;
}
</style>
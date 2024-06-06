<template>
  <div>
    <label for="cb1-input">
      State
    </label>
    <div class="combobox combobox-list">
      <div class="group">
        <input
          id="cb1-input"
          class="cb_edit"
          type="text"
          role="combobox"
          aria-autocomplete="both"
          aria-expanded="false"
          aria-controls="cb1-listbox"
        />
        <button
          type="button"
          id="cb1-button"
          aria-label="States"
          aria-expanded="false"
          aria-controls="cb1-listbox"
          tabindex="-1"
        >
          <svg width="18" height="16" aria-hidden="true" focusable="false" style="forced-color-adjust: auto">
            <polygon
              class="arrow"
              stroke-width="0"
              fill-opacity="0.75"
              fill="currentcolor"
              points="3,6 15,6 9,14"
            ></polygon>
          </svg>
        </button>
      </div>
      <ul id="cb1-listbox" role="listbox" aria-label="States">
        <li id="lb1-al" role="option">
          Alabama
        </li>
        <li id="lb1-ak" role="option">
          Alaska
        </li>
        <li id="lb1-as" role="option">
          American Samoa
        </li>
        <li id="lb1-az" role="option">
          Arizona
        </li>
        <li id="lb1-ar" role="option">
          Arkansas
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
/*
 *   This content is licensed according to the W3C Software License at
 *   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
 */

class ComboboxAutocomplete {
  constructor(comboboxNode, buttonNode, listboxNode) {
    this.comboboxNode = comboboxNode
    this.buttonNode = buttonNode
    this.listboxNode = listboxNode

    this.comboboxHasVisualFocus = false
    this.listboxHasVisualFocus = false

    this.hasHover = false

    this.isNone = false
    this.isList = false
    this.isBoth = false

    this.allOptions = []

    this.option = null
    this.firstOption = null
    this.lastOption = null

    this.filteredOptions = []
    this.filter = ""

    var autocomplete = this.comboboxNode.getAttribute("aria-autocomplete")

    if (typeof autocomplete === "string") {
      autocomplete = autocomplete.toLowerCase()
      this.isNone = autocomplete === "none"
      this.isList = autocomplete === "list"
      this.isBoth = autocomplete === "both"
    } else {
      // default value of autocomplete
      this.isNone = true
    }

    this.comboboxNode.addEventListener("keydown", this.onComboboxKeyDown.bind(this))
    this.comboboxNode.addEventListener("keyup", this.onComboboxKeyUp.bind(this))
    this.comboboxNode.addEventListener("click", this.onComboboxClick.bind(this))
    this.comboboxNode.addEventListener("focus", this.onComboboxFocus.bind(this))
    this.comboboxNode.addEventListener("blur", this.onComboboxBlur.bind(this))

    document.body.addEventListener("pointerup", this.onBackgroundPointerUp.bind(this), true)

    // initialize pop up menu

    this.listboxNode.addEventListener("pointerover", this.onListboxPointerover.bind(this))
    this.listboxNode.addEventListener("pointerout", this.onListboxPointerout.bind(this))

    // Traverse the element children of domNode: configure each with
    // option role behavior and store reference in.options array.
    var nodes = this.listboxNode.getElementsByTagName("LI")

    for (var i = 0; i < nodes.length; i++) {
      var node = nodes[i]
      this.allOptions.push(node)

      node.addEventListener("click", this.onOptionClick.bind(this))
      node.addEventListener("pointerover", this.onOptionPointerover.bind(this))
      node.addEventListener("pointerout", this.onOptionPointerout.bind(this))
    }

    this.filterOptions()

    // Open Button

    var button = this.comboboxNode.nextElementSibling

    if (button && button.tagName === "BUTTON") {
      button.addEventListener("click", this.onButtonClick.bind(this))
    }
  }

  getLowercaseContent(node) {
    return node.textContent.toLowerCase()
  }

  getNormalisedLowercaseContent(node) {
    return this.getLowercaseContent(node).trim()
  }

  isOptionInView(option) {
    var bounding = option.getBoundingClientRect()
    return (
      bounding.top >= 0 &&
      bounding.left >= 0 &&
      bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
    )
  }

  setActiveDescendant(option) {
    if (option && this.listboxHasVisualFocus) {
      this.comboboxNode.setAttribute("aria-activedescendant", option.id)
      if (!this.isOptionInView(option)) {
        option.scrollIntoView({ behavior: "smooth", block: "nearest" })
      }
    } else {
      this.comboboxNode.setAttribute("aria-activedescendant", "")
    }
  }

  setValue(value) {
    this.filter = value
    this.comboboxNode.value = this.filter
    this.comboboxNode.setSelectionRange(this.filter.length, this.filter.length)
    this.filterOptions()
  }

  setOption(option, flag) {
    if (typeof flag !== "boolean") {
      flag = false
    }

    if (option) {
      this.option = option
      this.setCurrentOptionStyle(this.option)
      this.setActiveDescendant(this.option)

      if (this.isBoth) {
        this.comboboxNode.value = this.option.textContent
        if (flag) {
          this.comboboxNode.setSelectionRange(this.option.textContent.length, this.option.textContent.length)
        } else {
          this.comboboxNode.setSelectionRange(this.filter.length, this.option.textContent.length)
        }
      }
    }
  }

  setVisualFocusCombobox() {
    this.listboxNode.classList.remove("focus")
    this.comboboxNode.parentNode.classList.add("focus") // set the focus class to the parent for easier styling
    this.comboboxHasVisualFocus = true
    this.listboxHasVisualFocus = false
    this.setActiveDescendant(false)
  }

  setVisualFocusListbox() {
    this.comboboxNode.parentNode.classList.remove("focus")
    this.comboboxHasVisualFocus = false
    this.listboxHasVisualFocus = true
    this.listboxNode.classList.add("focus")
    this.setActiveDescendant(this.option)
  }

  removeVisualFocusAll() {
    this.comboboxNode.parentNode.classList.remove("focus")
    this.comboboxHasVisualFocus = false
    this.listboxHasVisualFocus = false
    this.listboxNode.classList.remove("focus")
    this.option = null
    this.setActiveDescendant(false)
  }

  // ComboboxAutocomplete Events

  filterOptions() {
    // do not filter any options if autocomplete is none
    if (this.isNone) {
      this.filter = ""
    }

    var option = null
    var currentOption = this.option
    var filter = this.filter.toLowerCase()

    this.filteredOptions = []
    this.listboxNode.innerHTML = ""

    for (var i = 0; i < this.allOptions.length; i++) {
      option = this.allOptions[i]
      if (filter.length === 0 || this.getNormalisedLowercaseContent(option).indexOf(filter) === 0) {
        this.filteredOptions.push(option)
        this.listboxNode.appendChild(option)
      }
    }

    // Use populated options array to initialize firstOption and lastOption.
    var numItems = this.filteredOptions.length
    if (numItems > 0) {
      this.firstOption = this.filteredOptions[0]
      this.lastOption = this.filteredOptions[numItems - 1]

      if (currentOption && this.filteredOptions.indexOf(currentOption) >= 0) {
        option = currentOption
      } else {
        option = this.firstOption
      }
    } else {
      this.firstOption = null
      option = null
      this.lastOption = null
    }
    return option
  }

  setCurrentOptionStyle(option) {
    for (var i = 0; i < this.filteredOptions.length; i++) {
      var opt = this.filteredOptions[i]
      if (opt === option) {
        opt.setAttribute("aria-selected", "true")
        if (this.listboxNode.scrollTop + this.listboxNode.offsetHeight < opt.offsetTop + opt.offsetHeight) {
          this.listboxNode.scrollTop = opt.offsetTop + opt.offsetHeight - this.listboxNode.offsetHeight
        } else if (this.listboxNode.scrollTop > opt.offsetTop + 2) {
          this.listboxNode.scrollTop = opt.offsetTop
        }
      } else {
        opt.removeAttribute("aria-selected")
      }
    }
  }

  getPreviousOption(currentOption) {
    if (currentOption !== this.firstOption) {
      var index = this.filteredOptions.indexOf(currentOption)
      return this.filteredOptions[index - 1]
    }
    return this.lastOption
  }

  getNextOption(currentOption) {
    if (currentOption !== this.lastOption) {
      var index = this.filteredOptions.indexOf(currentOption)
      return this.filteredOptions[index + 1]
    }
    return this.firstOption
  }

  /* MENU DISPLAY METHODS */

  doesOptionHaveFocus() {
    return this.comboboxNode.getAttribute("aria-activedescendant") !== ""
  }

  isOpen() {
    return this.listboxNode.style.display === "block"
  }

  isClosed() {
    return this.listboxNode.style.display !== "block"
  }

  hasOptions() {
    return this.filteredOptions.length
  }

  open() {
    this.listboxNode.style.display = "block"
    this.comboboxNode.setAttribute("aria-expanded", "true")
    this.buttonNode.setAttribute("aria-expanded", "true")
  }

  close(force) {
    if (typeof force !== "boolean") {
      force = false
    }

    if (force || (!this.comboboxHasVisualFocus && !this.listboxHasVisualFocus && !this.hasHover)) {
      this.setCurrentOptionStyle(false)
      this.listboxNode.style.display = "none"
      this.comboboxNode.setAttribute("aria-expanded", "false")
      this.buttonNode.setAttribute("aria-expanded", "false")
      this.setActiveDescendant(false)
      this.comboboxNode.parentNode.classList.add("focus")
    }
  }

  /* combobox Events */

  onComboboxKeyDown(event) {
    var flag = false,
      altKey = event.altKey

    if (event.ctrlKey || event.shiftKey) {
      return
    }

    switch (event.key) {
      case "Enter":
        if (this.listboxHasVisualFocus) {
          this.setValue(this.option.textContent)
        }
        this.close(true)
        this.setVisualFocusCombobox()
        flag = true
        break

      case "Down":
      case "ArrowDown":
        if (this.filteredOptions.length > 0) {
          if (altKey) {
            this.open()
          } else {
            this.open()
            if (this.listboxHasVisualFocus || (this.isBoth && this.filteredOptions.length > 1)) {
              this.setOption(this.getNextOption(this.option), true)
              this.setVisualFocusListbox()
            } else {
              this.setOption(this.firstOption, true)
              this.setVisualFocusListbox()
            }
          }
        }
        flag = true
        break

      case "Up":
      case "ArrowUp":
        if (this.hasOptions()) {
          if (this.listboxHasVisualFocus) {
            this.setOption(this.getPreviousOption(this.option), true)
          } else {
            this.open()
            if (!altKey) {
              this.setOption(this.lastOption, true)
              this.setVisualFocusListbox()
            }
          }
        }
        flag = true
        break

      case "Esc":
      case "Escape":
        if (this.isOpen()) {
          this.close(true)
          this.filter = this.comboboxNode.value
          this.filterOptions()
          this.setVisualFocusCombobox()
        } else {
          this.setValue("")
          this.comboboxNode.value = ""
        }
        this.option = null
        flag = true
        break

      case "Tab":
        this.close(true)
        if (this.listboxHasVisualFocus) {
          if (this.option) {
            this.setValue(this.option.textContent)
          }
        }
        break

      case "Home":
        this.comboboxNode.setSelectionRange(0, 0)
        flag = true
        break

      case "End":
        var length = this.comboboxNode.value.length
        this.comboboxNode.setSelectionRange(length, length)
        flag = true
        break

      default:
        break
    }

    if (flag) {
      event.stopPropagation()
      event.preventDefault()
    }
  }

  isPrintableCharacter(str) {
    return str.length === 1 && str.match(/\S| /)
  }

  onComboboxKeyUp(event) {
    var flag = false,
      option = null,
      char = event.key

    if (this.isPrintableCharacter(char)) {
      this.filter += char
    }

    // this is for the case when a selection in the textbox has been deleted
    if (this.comboboxNode.value.length < this.filter.length) {
      this.filter = this.comboboxNode.value
      this.option = null
      this.filterOptions()
    }

    if (event.key === "Escape" || event.key === "Esc") {
      return
    }

    switch (event.key) {
      case "Backspace":
        this.setVisualFocusCombobox()
        this.setCurrentOptionStyle(false)
        this.filter = this.comboboxNode.value
        this.option = null
        this.filterOptions()
        flag = true
        break

      case "Left":
      case "ArrowLeft":
      case "Right":
      case "ArrowRight":
      case "Home":
      case "End":
        if (this.isBoth) {
          this.filter = this.comboboxNode.value
        } else {
          this.option = null
          this.setCurrentOptionStyle(false)
        }
        this.setVisualFocusCombobox()
        flag = true
        break

      default:
        if (this.isPrintableCharacter(char)) {
          this.setVisualFocusCombobox()
          this.setCurrentOptionStyle(false)
          flag = true

          if (this.isList || this.isBoth) {
            option = this.filterOptions()
            if (option) {
              if (this.isClosed() && this.comboboxNode.value.length) {
                this.open()
              }

              if (this.getLowercaseContent(option).indexOf(this.comboboxNode.value.toLowerCase()) === 0) {
                this.option = option
                if (this.isBoth || this.listboxHasVisualFocus) {
                  this.setCurrentOptionStyle(option)
                  if (this.isBoth) {
                    this.setOption(option)
                  }
                }
              } else {
                this.option = null
                this.setCurrentOptionStyle(false)
              }
            } else {
              this.close()
              this.option = null
              this.setActiveDescendant(false)
            }
          } else if (this.comboboxNode.value.length) {
            this.open()
          }
        }

        break
    }

    if (flag) {
      event.stopPropagation()
      event.preventDefault()
    }
  }

  onComboboxClick() {
    if (this.isOpen()) {
      this.close(true)
    } else {
      this.open()
    }
  }

  onComboboxFocus() {
    this.filter = this.comboboxNode.value
    this.filterOptions()
    this.setVisualFocusCombobox()
    this.option = null
    this.setCurrentOptionStyle(null)
  }

  onComboboxBlur() {
    this.removeVisualFocusAll()
  }

  onBackgroundPointerUp(event) {
    if (
      !this.comboboxNode.contains(event.target) &&
      !this.listboxNode.contains(event.target) &&
      !this.buttonNode.contains(event.target)
    ) {
      this.comboboxHasVisualFocus = false
      this.setCurrentOptionStyle(null)
      this.removeVisualFocusAll()
      setTimeout(this.close.bind(this, true), 300)
    }
  }

  onButtonClick() {
    if (this.isOpen()) {
      this.close(true)
    } else {
      this.open()
    }
    this.comboboxNode.focus()
    this.setVisualFocusCombobox()
  }

  /* Listbox Events */

  onListboxPointerover() {
    this.hasHover = true
  }

  onListboxPointerout() {
    this.hasHover = false
    setTimeout(this.close.bind(this, false), 300)
  }

  // Listbox Option Events

  onOptionClick(event) {
    this.comboboxNode.value = event.target.textContent
    this.close(true)
  }

  onOptionPointerover() {
    this.hasHover = true
    this.open()
  }

  onOptionPointerout() {
    this.hasHover = false
    setTimeout(this.close.bind(this, false), 300)
  }
}

// TODO:
// how to auto select first option?
// Define this component with props : label, items etc
// Pass option to parent with $emit
// Replace region/department select (make own components wrapping this?)
// Replace city field : API list?
// Dsfr styling

export default {
  name: "WaiCombobox",
  mounted() {
    var comboboxes = document.querySelectorAll(".combobox-list")

    for (var i = 0; i < comboboxes.length; i++) {
      var combobox = comboboxes[i]
      var comboboxNode = combobox.querySelector("input")
      var buttonNode = combobox.querySelector("button")
      var listboxNode = combobox.querySelector('[role="listbox"]')
      new ComboboxAutocomplete(comboboxNode, buttonNode, listboxNode)
    }
  },
}
</script>

<style scoped>
.combobox-list {
  position: relative;
}

.combobox .group {
  display: inline-flex;
  padding: 4px;
  cursor: pointer;
}

.combobox input,
.combobox button {
  background-color: white;
  color: black;
  box-sizing: border-box;
  height: 30px;
  padding: 0;
  margin: 0;
  vertical-align: bottom;
  border: 1px solid gray;
  position: relative;
  cursor: pointer;
}

.combobox input {
  width: 150px;
  border-right: none;
  outline: none;
  font-size: 87.5%;
  padding: 1px 3px;
}

.combobox button {
  width: 19px;
  border-left: none;
  outline: none;
  color: rgb(0 90 156);
}

.combobox button[aria-expanded="true"] svg {
  transform: rotate(180deg) translate(0, -3px);
}

ul[role="listbox"] {
  margin: 0;
  padding: 0;
  position: absolute;
  left: 4px;
  top: 34px;
  list-style: none;
  background-color: white;
  display: none;
  box-sizing: border-box;
  border: 2px currentcolor solid;
  max-height: 250px;
  width: 168px;
  overflow: scroll;
  overflow-x: hidden;
  font-size: 87.5%;
  cursor: pointer;
  z-index: 99;
}

ul[role="listbox"] li[role="option"] {
  margin: 0;
  display: block;
  padding-left: 3px;
  padding-top: 2px;
  padding-bottom: 2px;
}

/* focus and hover styling */

.combobox .group.focus,
.combobox .group:hover {
  padding: 2px;
  border: 2px solid currentcolor;
  border-radius: 4px;
}

.combobox .group.focus polygon,
.combobox .group:hover polygon {
  fill-opacity: 1;
}

.combobox .group.focus input,
.combobox .group.focus button,
.combobox .group input:hover,
.combobox .group button:hover {
  background-color: #def;
}

[role="listbox"].focus [role="option"][aria-selected="true"],
[role="listbox"] [role="option"]:hover {
  background-color: #def;
  padding-top: 0;
  padding-bottom: 0;
  border-top: 2px solid currentcolor;
  border-bottom: 2px solid currentcolor;
}
</style>

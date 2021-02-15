<template>
        <div class="treemap">
          <svg :width="width+'%'" :height="84.5+'vh'" style="margin-left: 0%;" position="absolute" id="package">
            <g style="shape-rendering: crispEdges;" transform="translate(0,20)" v-if="selectedNode">
                <g class="children" v-for="(children, index) in selectedNode._children" :key="'c_' + index">

                  <rect v-for="(child, id) in children._children" class="child" :id="id" :key="id"
                    :height="(y(child.y1) - y(child.y0))+'%'"
                    :width="(x(child.x1) - x(child.x0))+'%'"
                    :x="x(child.x0)+'%'" :y="y(child.y0)+'%'">
                  </rect>

                  <rect class="parent" v-on:click="selectNode" :id="children.id" :key="children.id"
                    :x="x(children.x0)+'%'" :y="y(children.y0)+'%'"
                    :width="x(children.x1 - children.x0 + children.parent.x0)+'%'"
                    :height="y(children.y1 - children.y0 + children.parent.y0)+'%'"
                    :style="{ fill: color(index) }">

                    <!-- The title attribute -->
                    <title>{{ children.data.subject }} | {{`${getBytesToSize(children.value)}`}}</title>
                  </rect>

                  <!-- The visible square text element with the title and value of the child node -->
                  <text dy="1em" :key="'t_' + index" :x="x(children.x0) + 6" :y="y(children.y0) + 6"
                    style="fill-opacity: 1;" v-if="!isSquareTooSmall(children)">
                    {{ children.data.subject }}
                  </text>

                  <text dy="2.25em" :key="'k_' + index" :x="x(children.x0) + 6" :y="y(children.y0) + 6"
                    style="fill-opacity: 1;" v-if="!isSquareTooSmall(children)">
                    {{ `${getBytesToSize(children.value)}` }}
                  </text>
                </g>

              <g class="grandparent">
                <rect :height="margin.top+'%'" :width="width+'%'" :y="(margin.top * -1)+'%'" v-on:click="selectNode"
                  :id="parentId">
                </rect>
                <text dy=".65em" x="6" y="-14">
                  {{ selectedNode.id }}
                </text>
              </g>
            </g>
          </svg>
        </div>
</template>

<script>
import {
  scaleLinear,
  scaleOrdinal
} from 'd3-scale'
import {
  schemeCategory10
} from 'd3-scale-chromatic'
import {
  json
} from 'd3-request'
import {
  hierarchy,
  treemap
} from 'd3-hierarchy'
import byteSize from 'byte-size'

let d3 = {
  scaleLinear: scaleLinear,
  scaleOrdinal: scaleOrdinal,
  schemeCategory10: schemeCategory10,
  json: json,
  hierarchy: hierarchy,
  treemap: treemap,
}


export default {
  name: 'Treemap',
  data() {
    return {
      jsonData: null,
      rootNode: {},
      margin: {
        top: 20,
        right: 0,
        bottom: 0,
        left: 0
      },
      width: 100,
      height: 100,
      selected: null,
      color: {},
    }
  },
  props: {
    threads_prop: Object
  },
  watch: {
    selectedNode() {
      console.log('The selected node changed...')
    },
    threads_prop() {
      var that = this
      if (that.threads_prop) {
        that.jsonData = that.threads_prop
        that.initialize()
        that.accumulate(that.rootNode, that)
        that.treemap(that.rootNode)
      }
    }
  },
  mounted() {
    var that = this
    that.color = d3.scaleOrdinal(d3.schemeCategory10)
  },
  computed: {
    parentId() {
      if (this.selectedNode.parent === undefined || this.selectedNode.parent === null) {
        return this.selectedNode.id
      } else {
        return this.selectedNode.parent.id
      }
    },
    x() {
      return d3.scaleLinear()
        .domain([0, this.width])
        .range([0, this.width])
    },
    y() {
      return d3.scaleLinear()
        .domain([0, this.height - this.margin.top - this.margin.bottom])
        .range([0, this.height - this.margin.top - this.margin.bottom])
    },
    treemap() {
      return d3.treemap()
        .size([this.width, this.height])
        .round(false)
        .paddingInner(0)
    },
    selectedNode() {
      let node = null

      if (this.selected) {
        let nd = this.getNodeById(this.rootNode, this.selected, this)

        if (nd._children) {
          node = nd
        } else {
          node = nd.parent
        }
      } else {
        node = this.rootNode
      }

      this.x.domain([node.x0, node.x0 + (node.x1 - node.x0)])
      this.y.domain([node.y0, node.y0 + (node.y1 - node.y0)])

            if (d._children) {
                d.value = d._children.reduce(function (p, v) {
                    return p + context.accumulate(v, context)
                }, 0)
                return d.value
            } else {
                d.value = d.value
                return d.value
            }
        },
        // Helper method - gets a node by its id attribute
        getNodeById(node, id, context) {
            if (node.id === id) {
                return node
            } else if (node._children) {
                for (var i = 0; i < node._children.length; i++) {
                    var nd = context.getNodeById(node._children[i], id, context)
                    if (nd) {
                        return nd
                    }
                }
            }
        },
        // When a user clicks a square, changes the selected data attribute
        // which fires the computed selectedNode, which in turn finds the Node by the id of the square clicked
        // and the template reflects the changes
        selectNode(event) {
            this.selected = event.target.id
        },
        getBytesToSize(bytes) {
            return byteSize(bytes)
        },
        isSquareTooSmall(children){
          // console.log("y", this.y(children.y1 - children.y0 + children.parent.y0))
          // console.log("x", this.x(children.x1 - children.x0 + children.parent.x0))
          return this.y(children.y1 - children.y0 + children.parent.y0)*this.x(children.x1 - children.x0 + children.parent.x0) < 1000
        },
    }
  }
}
</script>

<style scoped>
text {
  pointer-events: none;
}

.grandparent text {
  font-weight: bold;
}

rect {
  fill: none;
  stroke: #fff;
}

rect.parent,
.grandparent rect {
  stroke-width: 2px;
}

.grandparent rect {
  fill: orange;
}

.grandparent:hover rect {
  fill: #ee9700;
}

.children rect.parent,
.grandparent rect {
  cursor: pointer;
}

.children rect.parent {
  fill: #bbb;
  fill-opacity: 0.94;
}

.children:hover rect.child {
  fill: #bbb;
}

.children text {
  font-size: 0.8em;
}

.grandparent text {
  font-size: 0.9em;
}

.samir {
  overflow: auto
}
</style>
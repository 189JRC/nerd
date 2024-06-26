<template>
  <div>
    <!-- <textarea v-model="text" placeholder="Enter text here..." class="block appearance-none w-full h-64 bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 rounded shadow leading-tight focus:outline-none focus:shadow-outline mb-4"></textarea>
    <br> -->
    <div class="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">

      <div class="flex justify-center">
        <input id="option1" name="options" type="radio" value="article" v-model="type_of_scrape"
          class="form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out" />
        <label for="option1" class="ml-2 mr-2 block text-gray-700">Article</label>

        <input id="option2" name="options" type="radio" value="youtube_transcript" v-model="type_of_scrape"
          class="form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out" />
        <label for="option2" class="ml-2 mr-2 block text-gray-700">YouTube Transcript</label>

        <input id="option3" name="options" type="radio" value="twitter" v-model="type_of_scrape"
          class="form-radio h-4 w-4 text-blue-600 transition duration-150 ease-in-out" />
        <label for="option3" class="ml-2 mr-2 block text-gray-700">Twitter</label>
      </div>
      <!-- <div class="mt-4 text-center">
        <p>Selected Option: {{ data_source_option }}</p>
      </div> -->
    </div>

    <div class="flex items-center mt-5 p-4 max-w-lg mx-auto dark:bg-white rounded-l shadow-md">
      <input v-model="target_url" placeholder="Enter URL here"
        class="flex-grow p-3 rounded-l-lg border border-gray-300 focus:outline-none focus:border-blue-500" />
      <button @click="fetch_text_data"
        class="ml-2 px-4 py-3 bg-blue-500 text-white rounded-r-lg hover:bg-blue-700 focus:outline-none">
        Fetch
      </button>
      <!--USE SVG TO GUIDE USER-->
      <!-- <svg height="100" width="100" >
        <circle cx="50" cy="50" r="20" stroke="black" stroke-width="1" fill="none"/>
      </svg> -->

    </div>
    <br>
    <hr>
    <div class="flex justify-center">
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
        @click="process_text_string_with_nlp_model">Process Text</button>
      <button class="bg-orange-500 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
        @click="render_network">build
        network</button>
      <button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mt-5 p-4 justify-center"
        @click="highlightText">highlight text</button>
    </div>
  </div>
  <br>
  <hr>
  <br>
  <div ref="highlighted_text_container" @mouseup="handle_mouse_selection"
    class="isolate w-4/5 max-h-screen rounded-xl pl-5 pb-5 pr-5 bg-white shadow-lg ring-1 mx-auto overflow-auto">
    <br>
    
    <div v-if="highlighted_text" v-html="highlighted_text"></div>
    <div v-else>{{ text }}</div>
    <div v-if="show_popup" :style="popup_style" class="popup">
      <p><strong>{{ popup_text }}</strong></p>
      <hr>
      <br>
      <button class="bg-green-500" @click="mark_as_significant">Significant?</button><br>
      <button class="bg-orange-500" @click="make_insignificant">Not significant?</button>
    </div>
  </div>


  <div class="flex">
    <div class="mt-5 p-4 max-w-md mx-auto dark:bg-gray-200 rounded-l shadow-md">
      <h5 class="text-dark-grey text-2xl">All entities</h5>
      <ul>
        <li v-for="entity in entities" :key="entity.text">
          {{ entity }}
        </li>
      </ul>
    </div>
    <div class="mt-5 p-4 max-w-md mx-auto dark:bg-gray-200 rounded-l shadow-md">
      <h5 class="text-dark-grey text-2xl">Significant entities</h5>
      <ul>
        <li v-for="significant_entity in significant_entities" :key="significant_entity.text">
          {{ significant_entity }}
        </li>
      </ul>
    </div>
    <div class="mt-5 p-4 max-w-md mx-auto dark:bg-gray-200 rounded-l shadow-md">
      <h5 class="text-dark-grey text-2xl">Diagram Entities</h5>
      <ul>
        <li v-for="entity in diagram_entities" :key="entity.text">
          {{ entity }}
        </li>
      </ul>
    </div>
  </div>

  <div id="network" class="w-4/5 h-500 border border-blue-500 rounded mx-auto my-4"
    style="height: 500px; width: 1000px"></div>
</template>
<script>
import { Network, DataSet } from 'vis-network/standalone/umd/vis-network.min.js';


export default {
  data() {
    return {
      text: "The family and friends of a British teenager who is missing in Tenerife have shared a picture of a 'possible sighting' of the teenager as the desperate search to find him goes on. The search for Jay Slater is now into its second week after the 19-year-old was reported missing by his friends on the Spanish island last Monday (June 17). The teenager reportedly walked off alone into a mountainous area in the Rural de Teno Park, close to the village of Masca, after leaving an Airbnb rental apartment where he had stayed with two people he met at the NRG music festival. Urgent searches, involving Civil Guard officers, firefighters and mountain rescuers, have been ongoing in the vast area since his disappearance",
      entities: [],
      selected_model: "spacy",
      show_popup: false,
      significant_entities: [],
      data_entity_selected_for_relevance: "ZZZ",
      diagram_entities: [{ "label": "GPE", "name": "Tenerife" },
      { "label": "PERSON", "name": "Jay Slater" },
      { "label": "DATE", "name": "19-year-old" }],
      target_url: "https://www.telegraph.co.uk/world-news/2024/06/24/jay-slater-missing-update-parents-release-cctv-tenerife/",
      highlighted_text: null,
      selected_text: null,
      youtube_url: null,
      type_of_scrape: "youtube_transcript",
      data_source_option: null,
    };
  },
  // mounted() {
  //   document.addEventListener('selectionchange', this.handle_selection_change);
  // },
  // beforeUnmount() {
  //   document.removeEventListener('selectionchange', this.handle_selection_change);
  // },
  updated() {
    this.addEventListeners();
  },
  methods: {
    // TODO:1: Put all fetch calls into seperate JS object file
    reset_state() {
      this.highlighted_text = ""
      this.text = ""
    },
    async process_text_string_with_nlp_model() {
      try {
        const response = await fetch('http://localhost:5000/process', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: this.text, model: this.selected_model })
        });

        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        this.entities = data;
        this.make_significant_entities(data)
      } catch (error) {
        console.error('There was a problem with the fetch. Error:', error);
      }
    },
    async fetch_text_data() {
      console.log("fetch_text_data called on: ", this.target_url)
      console.log("type of scrape: ", this.type_of_scrape)
      this.reset_state()
      try {
        const response = await fetch('http://localhost:5000/scrape', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ url: this.target_url, type_of_scrape: this.type_of_scrape })
        });

        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        console.log(data.article_text)
        this.text = data.article_text;

      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    },
    // async fetch_youtube_transcript() {
    //   console.log("fetch_article_data_called on: ", "https://www.youtube.com/watch?v=1zErA1Igtow") 
    //   try {
    //     const response = await fetch('http://localhost:5000/scrape_youtube_transcript', {
    //       method: 'POST',
    //       headers: {
    //         'Content-Type': 'application/json'
    //       },
    //       body: JSON.stringify({ target_url: "1zErA1Igtow" })
    //     });

    //     if (!response.ok) {
    //       throw new Error('Network response was not ok ' + response.statusText);
    //     }

    //     const data = await response.json();
    //     this.text = data.transcript_text;

    //   } catch (error) {
    //     console.error('There was a problem with the fetch operation:', error);
    //   }
    // },
    make_significant_entities(entity_objects) {
      entity_objects.forEach((entity) => {
        this.significant_entities.push(entity);
      });
    },
    render_network() {
      const nodes = [];
      const edges = [];
      const nodeMap = new Map(); // To track node ids

      // Function to add nodes if they don't exist
      const addNode = (id, label) => {
        if (nodeMap.has(id) == false) {
          nodeMap.set(id, { id: nodeMap.size + 1, label });
          nodes.push({ id: nodeMap.size, label });
        }
      };

      // Process entities to create nodes
      console.log("raw", this.diagram_entities[0])

      ///////////////////////
      //this if fast track
      let parsedEntities = this.diagram_entities
      //this if user selection

      // let parsedEntities = []
      // this.diagram_entities.forEach((entity) => {
      //   parsedEntities.push(JSON.parse(entity))
      // })

      ///////////////////////
      console.log("processed", parsedEntities)
      parsedEntities.forEach((entity) => {
        console.log(entity, entity.name, entity.label)
        addNode(entity.name, `${entity.label}\n(${entity.name})`);
      });

      // Create edges based on narrative structure
      let lastEntity = null;
      parsedEntities.forEach((entity) => {
        if (lastEntity) {
          edges.push({
            from: nodeMap.get(lastEntity.name).id,
            to: nodeMap.get(entity.name).id
          });
        }
        lastEntity = entity;
      });

      const container = document.getElementById('network');
      const data = {
        nodes: nodes,
        edges: edges
      };
      const options = {
        nodes: {
          shape: 'dot',
          size: 10
        },

        physics: {
          stabilization: {
            enabled: true,
            iterations: 200,
            updateInterval: 25
          },
          solver: 'barnesHut',
          barnesHut: {
            gravitationalConstant: -5000,
            centralGravity: 0.1,
            springLength: 95,
            springConstant: 0.01,
            damping: 0.89,
            avoidOverlap: 0.5
          }
        },
        manipulation: {
          enabled: true,
          addNode: function (nodeData, callback) {
            nodeData.label = "New Node";
            callback(nodeData);
          },
          editNode: function (nodeData, callback) {
            //TODO: Make this draggable/ dropable
            nodeData.label = prompt("Enter new label", nodeData.label);
            callback(nodeData);
          },
          addEdge: function (edgeData, callback) {
            if (edgeData.from !== edgeData.to) {
              alert("Cannot connect node to itself.");
              callback(edgeData);
            }
          },
          editEdge:
            function (edgeData, callback) {
              // Prompt the user for a new label for the edge
              const newLabel = prompt("Enter new label for the edge:", edgeData.label || "");

              // If a label is provided, set it on the edgeData
              if (newLabel !== null) {
                edgeData.label = newLabel;
              }

              // Call the callback function with the updated edgeData
              callback(edgeData);
            },
          // {
          //   editWithoutDrag: function (data, callback) {
          //     callback(data);
          //   }
          // },
          deleteNode: function (data, callback) {
            callback(data);
          },
          deleteEdge: function (data, callback) {
            callback(data);
          },
          controlNodeStyle: {
            // Control node style for editing edges
            shape: "dot",
            size: 6,
            color: {
              background: "red",
              border: "black",
            },
            borderWidth: 2,
            borderWidthSelected: 2,
          },
        }
      };
      new Network(container, data, options);
    },
    highlightText() {
      console.log("highlightText called")
      let highlighted = this.text;

      this.entities.forEach(entity => {
        const regex = new RegExp(`\\b${entity.name}\\b`, 'g');
        console.log(entity.name)
        const replacement = `<span class="indicator" data-entity='${JSON.stringify(entity)}'>${entity.name}</span>`;
        highlighted = highlighted.replace(regex, replacement);
      });
      this.highlighted_text = highlighted;


    },
    handle_selection_change() {
      const selection = document.getSelection()
      const selected_text = selection.toString();
      console.log(selected_text)
    },
    addEventListeners() {
      const indicators = this.$refs.highlighted_text_container.querySelectorAll('.indicator');
      this.$nextTick(() => { //next tick defers execution
        indicators.forEach(indicator => {
          indicator.removeEventListener('click', this.handleIndicatorClick);
          indicator.addEventListener('click', this.handleIndicatorClick);
        });
      });
    },
    handleIndicatorClick(event) {
      this.popup_text = event.target.textContent;
      this.data_entity_selected_for_relevance = event.target.getAttribute("data-entity")
      this.show_popup = true;
      this.popup_style = {
        position: 'absolute',
        top: `${event.clientY}px`,
        left: `${event.clientX}px`
      };
    },
    mark_as_significant() {
      // popup text is the highlighted word!¬
      console.log(this.popup_text)
      const new_significant_object = {
        label: "SIGNIFICANT",
        name: `${this.popup_text}`
      }
      this.diagram_entities.push(new_significant_object) //`{"label":"SIGNIFICANT", "name":"${this.popup_text}"}`)
      this.entities.push(new_significant_object) //`{"label":"SIGNIFICANT", "name":"${this.popup_text}"}`)
      this.highlightText()
      this.closePopup();
    },
    dismiss() {
      if (this.currentSpan) {
        this.currentSpan.classList.add('dismissed');
      }
      this.closePopup();
    },
    make_insignificant() {
      // TODO: might be less bug prone to resort the ents list with filter method here instead.
      // BIG TODO: Need to gether bunch these terms up and send them to the back end to make search queries out of.
      console.log(this.diagram_entities)
      for (let ent_index = 0; ent_index < this.diagram_entities.length; ent_index++) {
        console.log(this.diagram_entities[ent_index])
        if (this.diagram_entities[ent_index].name == this.popup_text) {
          console.log("found")
          this.diagram_entities.splice(ent_index, 1)
        }
      }
      for (let ent_index = 0; ent_index < this.entities.length; ent_index++) {
        console.log(this.entities[ent_index])
        if (this.entities[ent_index].name == this.popup_text) {
          console.log("found")
          this.entities.splice(ent_index, 1)
        }
      }
      this.highlightText()
      console.log(this.popup_text)
      this.closePopup();
    },
    closePopup() {
      this.show_popup = false;
      this.currentSpan = null;
    },
    handle_mouse_selection(event) {
      console.log("Squeek!")
      console.log(event)
      const selection = document.getSelection();
      const selected_text = selection.toString();
      if (selected_text.length < 3) {
        return
      } else {
        console.log(selected_text)
        this.show_popup = true
        this.popup_text = selected_text
        this.popup_style = {
          position: 'absolute',
          top: `${event.clientY}px`,
          left: `${event.clientX}px`
        };
      }
    }
  }
};
</script>
<style>
.significant {
  background-color: green;
}

.person {
  background-color: pink;
}

.gpe {
  background-color: pink;
}

.date {
  background-color: pink;
}

.loc {
  background-color: pink;
}

.indicator {
  background-color: pink;
}

.popup {
  background-color: white;
  border: 1px solid #ccc;
  padding: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}
</style>
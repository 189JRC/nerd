
class Investigation {
    constructor(domain_origin) {
        console.log("INV CREATED")
        this.domain_origin = domain_origin
        this.investigation = 'investigation'
        this.text_chunks = []
        this.current_chunk = ""
        this.selected_model = "spacy"
        this.significant_entities = []
        this.entities = []
        this.significant_details = []
        this.vector_comparison_metadata = ["NO DATA"]
        
    }
    async get_document_records() {
      try {
          const response = await fetch('http://localhost:5000/get_document_records', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            },
            // body: JSON.stringify({ text: "text" })
          });
  
          if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
          }
  
          const document_record_metadata = await response.json();
          return document_record_metadata
          // this.make_significant_entities(data)
  
        } catch (error) {
          console.error('There was a problem with the fetch. Error:', error);
        }
      }
    reset_state() {
        this.highlighted_text = ""
        this.text_chunks = ""
    }
    async fetch_text_data(target_url, type_of_scrape, string_to_vectorise=null) {
        // console.log("fetch_text_data called on:", target_url)
        // console.log("type of scrape: ", type_of_scrape)
        this.reset_state()
        if (string_to_vectorise == null) {
          var body = JSON.stringify({ url: target_url, type_of_scrape: type_of_scrape })
        } else if (string_to_vectorise != null) {
          var body = JSON.stringify({ url: null, type_of_scrape: type_of_scrape, string_for_vector_comparison: string_to_vectorise, params: "none yet" })
        }
        try {
            
            const response = await fetch(`${this.domain_origin}/triage_request`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
               
                body: body
                
            });

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            if (string_to_vectorise == null) {
            const data = await response.json();
            
            // article text is now a list of
            this.text_chunks = data.article_text;
            this.current_chunk = this.text_chunks[0]
            } else if (string_to_vectorise != null) {
              const vector_comparison_metadata = await response.json();
              this.vector_comparison_metadata = vector_comparison_metadata;
              console.log(typeof(this.vector_comparison_metadata))
              console.log(this.vector_comparison_metadata.top_most_similar)
            }

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }
    // async fetch_vector_comparison_data(string_for_vector_comparison) {
    //   console.log("CALLED fetch_vector_comparison_data")
    //     try {
    //       const response = await fetch('http://localhost:5000/vector_similarity', {
    //         method: 'POST',
    //         headers: {
    //           'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({ string_for_vector_comparison: string_for_vector_comparison, params: "none yet" })
    //       });
  
    //       if (!response.ok) {
    //         throw new Error('Network response was not ok ' + response.statusText);
    //       }
  
    //       const vector_comparison_metadata = await response.json();
    //       this.vector_comparison_metadata = vector_comparison_metadata;
    //       // this.make_significant_entities(data)
  
    //     } catch (error) {
    //       console.error('There was a problem with the fetch. Error:', error);
    //     }

    // }
    async process_text_string_with_nlp_model() {
        console.log("CALLED process_text_string_with_nlp_model")
        try {
          const response = await fetch('http://localhost:5000/process', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: this.current_chunk, model: this.selected_model })
          });
  
          if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
          }
  
          const data = await response.json();
          this.entities = data;
          // this.make_significant_entities(data)
  
        } catch (error) {
          console.error('There was a problem with the fetch. Error:', error);
        }
      }
    reset_state() {
        this.highlighted_text = ""
        this.text_chunks = ""
    }
    // make_significant_entities(entity_objects) {
    //     entity_objects.forEach((entity) => {
    //       this.significant_entities.push(entity);
    //     });
    //   }
}

export default Investigation
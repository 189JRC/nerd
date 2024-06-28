
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
        
    }
    async fetch_text_data(target_url, type_of_scrape) {
        console.log("fetch_text_data called on: ", target_url)
        console.log("type of scrape: ", type_of_scrape)
        this.reset_state()
        try {
            console.log("origin==", this.domain_origin)
            const response = await fetch(`${this.domain_origin}/scrape`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: target_url, type_of_scrape: type_of_scrape })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            const data = await response.json();
            console.log(">", typeof (data.article_text))
            // article text is now a list of
            this.text_chunks = data.article_text;
            this.current_chunk = this.text_chunks[0]

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }
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
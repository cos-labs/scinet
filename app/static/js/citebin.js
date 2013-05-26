// modelview for the citation citebin

// class representing an author
function Author(data) {
    this.family = ko.observable(data.family);
    this.given = ko.observable(data.given);
}

// class representing a citation
function Citation(authors, title, container_title, date, raw_data, references) {
}

function CitationModel(authors) {
    // data
    var self = this;

    // local
    self.given = ko.observable("");
    self.family = ko.observable("");
    self.isManualEntry = ko.observable(false);
    self.isRawEntry = ko.observable(false);
    self.isReferenceEntry = ko.observable(false);

    // citation
    self.citation = new Citation(null, "", "","","","");
    self.citation.title = ko.observable("");
    self.citation.container_title = ko.observable("");
    self.citation.date = ko.observable("");
    self.citation.DOI = ko.observable("");
    self.citation.raw_data = ko.observable("");
    self.citation.references = ko.observable("");
    self.citation.authors = ko.observableArray(ko.utils.arrayMap(authors, function(author) {
        return { family: author.family, given: author.given };
    }));
    self.lastSavedJson = ko.observable("");

    // operators

    // toggle manual entry forms visible or invisible
    self.toggleManualEntry = function() {
        self.isManualEntry(!self.isManualEntry());
    };

    // toggle raw paste form visible or invisible
    self.toggleRawEntry = function() {
        self.isRawEntry(!self.isRawEntry());
    };

    // toggle reference form visible or invisible
    self.toggleReferenceEntry = function() {
        self.isReferenceEntry(!self.isReferenceEntry());
    };

    // returns true if submission is true
    self.isValidSubmission = function() {
        if (self.citation.title != "" ) {
            return true;
        }
    };

    // add author to authors
    self.addAuthor = function() {
        // push a new author with the current pages given/family name
        self.citation.authors.push(new Author({ given: this.given(), family: this.family() }));
        // reset the classes given/family name variables
        self.given("");
        self.family("");
    };
    // remove author from authors
    self.removeAuthor = function(author) { self.citation.authors.remove(author) };

    // converts data to json
    self.save = function() {
        console.log(ko.toJSON(self.citation))
        $.ajax("/citebin", {
            data: ko.toJSON(self.citation),
            type: "post", contentType: "application/json",
            // success function is a workaround for flask returning
            // redirect to the ajax call not the browser
            success: function(result) {
                alert("Thank you for your submission! " + result);
                window.location.href='citebin';
                }
        });
    };
}

ko.applyBindings(new CitationModel());
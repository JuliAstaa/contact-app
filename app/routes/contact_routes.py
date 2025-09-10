from flask import render_template, redirect, request, url_for, flash, Blueprint
from app.services.contact_services import ContactServices

class ContactRoutes:
    def __init__(self):
        self.contact: Blueprint = Blueprint('contact', __name__)
        self.service = ContactServices()
        self.home()
        self.add()
        self.edit()
        self.delete()

    def home(self):
        @self.contact.route("/")
        def index():
            return render_template("index.html", datas = self.service.get_all_contact())
    
    def add(self):
        @self.contact.route("/add", methods=['GET', 'POST'])
        def add_contact():
            if request.method == "POST":
                f_name = request.form['f_name'].strip()
                l_name = request.form['l_name'].strip()
                phone_number = request.form['phone_number'].strip()
                email = request.form['email'].strip()

                is_created = ContactServices().create_contact(phone_number=phone_number, f_name=f_name, l_name=l_name, email=email)

                if is_created:
                    flash("Create success", "success")
                    return redirect(url_for("contact.index"))
                else:
                    flash("Failed to create", "failed")
                    return redirect(url_for("contact.add_contact"))
            
            return render_template("add.html")
    
    def edit(self):
        @self.contact.route("/edit/<int:id>", methods=['GET', 'POST'])
        def edit_contact(id):
            user = ContactServices().get_data_by_id(id)

            if request.method == "POST":
                f_name = request.form['f_name'].strip()
                l_name = request.form['l_name'].strip()
                phone_number = request.form['phone_number'].strip()
                email = request.form['email'].strip()

                is_edited = ContactServices().edit_contact(user=user, phone_number=phone_number, f_name=f_name, l_name=l_name, email=email)

                if is_edited:
                    flash("Edit success", 'success')
                    return redirect(url_for('contact.index'))
                else:
                    flash("Failed to edit", 'failed')
                    return redirect(url_for('contact.edit_contact', id=id))
                
            return render_template("edit.html", user=user)
    
    def delete(self):
        @self.contact.route('/delete/<int:id>', methods=["GET"])
        def delete_contact(id):
            user = ContactServices().get_data_by_id(id)

            is_deleted = ContactServices().remove_contact(user)

            if is_deleted:
                flash("Deleted", 'success')
            else:
                flash("Failed to delete", 'failed')
                
            return redirect(url_for('contact.index'))


def migrate_users_forward(apps, schema_editor):
    admin_user = apps.get_model('users_app','AdminUser')
    customer_user = apps.get_model('users_app' , 'CustomerUser')
    vendor_user = apps.get_model('users_app' , 'VendorUser')

    custom_user = apps.get_model('users_app','CustomUser')
    admin_profile = apps.get_model('users_app','AdminProfile')
    customer_profile = apps.get_model('users_app','CustomerProfile')
    vendor_profile = apps.get_model('users_app','VendorProfile')

    for admin in admin_user.objects.all():
        admin_profile.objects.create(
            user = custom_user.objects.create(
                firstname = admin.firstname,
                lastname = admin.lastname,
                email = admin.email,
                phone = admin.phone,
                password = admin.password,
                national_id = admin.national_id,
                address = admin.address,
                status = admin.status,
                joined_at = admin.joined_at
            ) ,
            admin_code = admin.admin_code,
            permissions_json = admin.permissions_json
        )

    for customer in custom_user.objects.all():
            customer_profile.objects.create(
                user = custom_user.objects.create(
                    firstname = customer.firstname,
                    lastname = customer.lastname,
                    email = customer.email,
                    phone = customer.phone,
                    password = customer.password,
                    national_id = customer.national_id,
                    address = customer.address,
                    status = customer.status,
                    joined_at = customer.joined_at
                ) ,
                zipcode = customer.zipcode,
                birth_date = customer.birth_date,
                gender = customer.gender,
                loyalty_points = customer.loyalty_points
            )

    for vendor in vendor_user.objects.all():
        vendor_profile.objects.create(
            user = custom_user.objects.create(
                firstname = vendor.firstname,
                lastname = vendor.lastname,
                email = vendor.email,
                phone = vendor.phone,
                password = vendor.password,
                national_id = vendor.national_id,
                address = vendor.address,
                status = vendor.status,
                joined_at = vendor.joined_at
            ) ,
            shop_name = vendor.shop_name,
            shop_address = vendor.shop_address,
            shop_license_number = vendor.shop_license_number,
            shop_phone = vendor.shop_phone,
            rating = vendor.rating,
            is_verified = vendor.is_verified
        )
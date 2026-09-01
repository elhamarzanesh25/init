def migrate_users_forward(apps, schema_editor):
    admin_user = apps.get_model('users_app', 'AdminUser')
    customer_user = apps.get_model('users_app', 'CustomerUser')
    vendor_user = apps.get_model('users_app', 'VendorUser')

    custom_user = apps.get_model('users_app', 'CustomUser')
    admin_profile = apps.get_model('users_app', 'AdminProfile')
    customer_profile = apps.get_model('users_app', 'CustomerProfile')
    vendor_profile = apps.get_model('users_app', 'VendorProfile')

    print("AdminUser count:", admin_user.objects.count())
    print("CustomerUser count:", customer_user.objects.count())
    print("VendorUser count:", vendor_user.objects.count())

    def get_or_create_user(old_obj, is_staff=False, is_superuser=False):
        user, created = custom_user.objects.get_or_create(
            email=old_obj.email,
            defaults={
                'username': old_obj.email,
                'first_name': old_obj.firstname,
                'last_name': old_obj.lastname,
                'phone': old_obj.phone,
                'password': old_obj.password,
                'national_id': old_obj.national_id,
                'address': old_obj.address,
                'status': old_obj.status,
                'joined_at': old_obj.joined_at,
                'is_staff': is_staff,
                'is_superuser': is_superuser,
            },
        )
        if not created and (is_staff or is_superuser):
            changed = False
            if is_staff and not user.is_staff:
                user.is_staff = True
                changed = True
            if is_superuser and not user.is_superuser:
                user.is_superuser = True
                changed = True
            if changed:
                user.save(update_fields=['is_staff', 'is_superuser'])
        return user

    for admin in admin_user.objects.all():
        user = get_or_create_user(admin, is_staff=True, is_superuser=True)
        admin_profile.objects.get_or_create(
            user=user,
            defaults={
                'admin_code': admin.admin_code,
                'permissions_json': admin.permissions_json,
            },
        )

    for customer in customer_user.objects.all():
        user = get_or_create_user(customer)
        customer_profile.objects.get_or_create(
            user=user,
            defaults={
                'zipcode': customer.zipcode,
                'birth_date': customer.birth_date,
                'gender': customer.gender,
                'loyalty_points': customer.loyalty_points,
            },
        )

    for vendor in vendor_user.objects.all():
        user = get_or_create_user(vendor)
        vendor_profile.objects.get_or_create(
            user=user,
            defaults={
                'shop_name': vendor.shop_name,
                'shop_address': vendor.shop_address,
                'shop_license_number': vendor.shop_license_number,
                'shop_phone': vendor.shop_phone,
                'rating': vendor.rating,
                'is_verified': vendor.is_verified,
            },
        )
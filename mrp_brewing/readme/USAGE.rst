Models
~~~~~~~

mrp.bom - Bill of Material
--------------------------

The Bill of Material (BOM) describes the ingredients needed to create a product.
Here, it will only be a step in the general beer recipe.
For example it will tell you that you need 1g of yeast and 1hL of *mout* (?)
to create 1hL of *green* beer.

From the BOM, the user can create Manufacturing Orders.

NB: Bill of Material is *Nomenclature* in French.

mrp.production - Manufacturing Order
------------------------------------

Created from a BOM template, a Manufacturing Order (MO) is an actual step of production.
The steps are:

1. New
    - Instanciated from the BOM
2. Confirmed - Awaiting for raw material
    - ``move_lines`` are created for incoming materials
    - The button *book resources* (?) allows to book the needed resources.
3. Ready
    - Once all resources are booked, the MO goes to ready state.
    - Through the "Produce" button, moves the MO to the production state.
4. In Production
    - While producing the step, the brewer moves the ingredients from
      the *to consume* to the *consumed* columns by allocating a lot number to each
      product.
5. Done
6. Cancelled


brew.order - Brew Order
-----------------------

brew.declaration - Brew Declaration
-----------------------------------

Master Manufacturing Order
~~~~~~~~~~~~~~~~~~~~~~~~~~

Many steps are needed to produce a beer.
We want to link all the steps for a single beer together in order to:

* symplify the creation of the MO:
  from a *Master MO* (eg. Green [#]_ Pale Ale), all linked steps (ie. MO) are created.
* Link all these MO to a single lot number.
  The lot number is created for the Master Manufacturing Order and then propa

-> I still don't really get how lot number is linked to MO...

.. [#] The *Green* beer is an unmatured beer.
